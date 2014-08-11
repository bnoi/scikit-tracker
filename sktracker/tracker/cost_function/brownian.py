
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from . import AbstractCostFunction
from .gap_close import AbstractGapCloseCostFunction
from ...trajectories import Trajectories

__all__ = ["BrownianLinkCostFunction", "BrownianGapCloseCostFunction"]


class BrownianLinkCostFunction(AbstractCostFunction):
    """This class generates cost matrices for brownian motion
    trajectories.

    The cost between two position is given by the square of their
    distance

    Attributes
    ----------

    parameters: dict
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

    def __init__(self, parameters):
        """
        """

        _parameters = {'distance_metric': 'euclidean',
                       'max_speed': 1.,
                       'coords': ['x', 'y', 'z']}
        _parameters.update(parameters)

        super(BrownianLinkCostFunction, self).__init__(context={}, parameters=_parameters)

    def _build(self):
        """
        """

        # Get parameters
        coords = self.parameters['coords']
        distance_metric = self.parameters['distance_metric']
        max_speed = self.parameters['max_speed']

        # Check context
        pos_in = self.check_context('pos_in', pd.DataFrame)
        pos_out = self.check_context('pos_out', pd.DataFrame)

        # Chech vectors
        self.check_columns([pos_in, pos_out], list(coords) + ['t'])

        if pos_out.empty or pos_in.empty:
            return pd.DataFrame([])

        dt = pos_out['t'].iloc[0] - pos_in['t'].iloc[0]

        # Build matrix block
        distances = cdist(pos_in[coords].astype(np.float),
                          pos_out[coords].astype(np.float),
                          metric=distance_metric)

        distances /= np.abs(dt)
        distances[distances > max_speed] = np.nan
        distances = distances ** 2

        return distances


class BrownianGapCloseCostFunction(AbstractGapCloseCostFunction):
    """
    """

    def __init__(self, parameters):
        """
        """
        _parameters = {'distance_metric': 'euclidean',
                       'max_speed': 1.,
                       'coords': ['x', 'y', 'z']}
        _parameters.update(parameters)

        super(self.__class__, self).__init__(context={}, parameters=_parameters)

    def _build(self,):
        """
        """

        self.check_idxs_length()

        # Get parameters
        coords = self.parameters['coords']
        distance_metric = self.parameters['distance_metric']

        if distance_metric != 'euclidean':
            raise Exception("Only 'euclidean' distance are supported for now.")

        max_speed = self.parameters['max_speed']

        # Check context
        idxs_in = self.check_context('idxs_in', list)
        idxs_out = self.check_context('idxs_out', list)
        trajs = self.check_context('trajs', Trajectories)

        # Just in case the parent didn't do it
        trajs.relabel_fromzero('label', inplace=True)

        # Init 2d distances array
        mat = np.empty((len(trajs.labels),
                        len(trajs.labels)))
        mat.fill(np.nan)

        # Compute distance between all_pos_out and all_pos_in
        all_pos_in = trajs.loc[idxs_in]
        all_pos_out = trajs.loc[idxs_out]
        vecs = [(all_pos_in[c].values - all_pos_out[c].values) ** 2 for c in coords]
        all_dist = np.sqrt(np.sum(vecs, axis=0))

        # Get all dt
        all_dt = np.abs(all_pos_in['t'].values - all_pos_out['t'].values)

        # Compute speeds
        speeds = all_dist / all_dt

        # Remove speeds greater than 'max_speed'
        speeds[speeds > max_speed] = np.nan

        # Fill 2d distances array
        i_in = np.array(idxs_in)[:, 1].astype(int)
        i_out = np.array(idxs_out)[:, 1].astype(int)
        mat[i_in, i_out] = speeds

        mat = mat ** 2

        return mat
