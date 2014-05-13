
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
import scipy as sp

from scipy import interpolate

from . import AbstractCostFunction

__all__ = ["BasicDirectedLinkCostFunction"]


class BasicDirectedLinkCostFunction(AbstractCostFunction):
    """This class generates cost matrices for directed motion
    trajectories.

    The cost between two position is given by the square of their
    distance

    Attributes
    ----------

    paramters: dict
        Used by the `build` method, with the following keys:

        - 'distance_metric': a string, default 'euclidean',
          passed to `scipy.spatial.distance.cdist`
          (see this function documentation for more)

        - 'coords': a list of column names on which to compute the distance,
            default ['x', 'y', 'z']

        - 'max_speed': a float, default 1. All the values of the cost matrix
           for which the distance *divided by the time difference* is higher than
           this parameter's value are set to np.nan

    context: dict
        Context is used to store vectors.

        - pos_in: :class:`pandas.DataFrame`
            The object coordinates to link from

        - pos_out: :class:`pandas.DataFrame`
            The object coordinates to link to

    """

    def __init__(self, parameters, context={}):

        _parameters = {'max_speed': 1.,
                       'past_traj_time': 1,
                       'smooth_factor': 0,
                       'interpolation_order': 1,
                       'coords': ['x', 'y', 'z']}
        _parameters.update(parameters)

        super(self.__class__, self).__init__(context=context, parameters=_parameters)

    def _build(self):
        """
        """

        # Get parameters
        coords = self.parameters['coords']
        max_speed = self.parameters['max_speed']
        past_traj_time = self.parameters['past_traj_time']
        smooth_factor = self.parameters['smooth_factor']
        interpolation_order = self.parameters['interpolation_order']

        # Check context
        pos_in = self.check_context('pos_in', pd.DataFrame)
        pos_out = self.check_context('pos_out', pd.DataFrame)
        trajs = self.check_context('trajs', pd.DataFrame)

        # Chech vectors
        self.check_columns([pos_in, pos_out], list(coords) + ['t'])

        t_in = pos_in['t'].iloc[0]
        t_out = pos_out['t'].iloc[0]
        dt = t_out - t_in

        # Select trajectory from (current_time - past_traj_time) and current_time
        last_past_time = t_in - (past_traj_time)
        past_trajs = trajs[(trajs.t <= t_in) & (trajs.t > last_past_time)]
        past_trajs_grouped = past_trajs.groupby(level='label').groups
        past_trajs_grouped

        n_t_past_trajs = past_trajs.index.get_level_values('t_stamp').unique().shape[0]
        if n_t_past_trajs < 3:
            # Not enough timepoints
            # Fallback to only distance
            distances = sp.spatial.distance.cdist(pos_in[coords].astype(np.float),
                                                  pos_out[coords].astype(np.float),
                                                  metric='euclidean')

            distances /= np.abs(dt)
            distances[distances > max_speed] = np.nan
            distances = distances ** 2

            return distances

        # Compute past trajectories vector
        vecs_speed_in = {}

        for label, index in past_trajs_grouped.items():
            past_traj = past_trajs.loc[index]

            vec_speed_in = {}
            for coord in coords:

                if past_traj.shape[0] < 4:
                    # Not enough timepoint to interpolate
                    vec_speed_in[coord] = 0
                else:
                    # Compute the derivative using B-Spline interpolation at time point = t_in
                    tck = interpolate.splrep(past_traj.t.values,
                                             past_traj[coord].values,
                                             s=smooth_factor,
                                             k=interpolation_order)
                    splines = interpolate.splev(t_in, tck, der=1)
                    vec_speed_in[coord] = splines

            vecs_speed_in[label] = vec_speed_in

        vecs_speed_in = pd.DataFrame.from_dict(vecs_speed_in).T.astype(np.float)

        # Compute the matrix according to euclidean distance and angle between vectors
        distances = np.empty((pos_in.shape[0], pos_out.shape[0]))
        distances.fill(np.nan)

        for i, idx_in in enumerate(pos_in.index):

            vec_speed_in = vecs_speed_in.loc[idx_in]
            r_in = pos_in.loc[idx_in]

            for j, idx_out in enumerate(pos_out.index):

                r_out = pos_out.loc[idx_out]

                vec_speed_out = (r_out[coords] - r_in[coords]) / np.abs(dt)

                current_speed = np.linalg.norm(vec_speed_out)

                if current_speed > max_speed:
                    score = np.nan
                else:
                    score = np.dot(vec_speed_in, vec_speed_out)
                    score /= np.linalg.norm(vec_speed_in) * np.linalg.norm(vec_speed_out)
                    score = np.rad2deg(np.arccos(score))
                    if score > 90:
                        score = 180 - score
                    score *= current_speed

                distances[i, j] = score

        return distances
