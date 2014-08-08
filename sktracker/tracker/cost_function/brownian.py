
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, pdist

from . import AbstractCostFunction
from ...utils import print_progress
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

    def _build(self, progress_bar=False, progress_bar_out=None):
        """
        """

        self.check_idxs_length()

        # Get parameters
        coords = self.parameters['coords']
        distance_metric = self.parameters['distance_metric']
        max_speed = self.parameters['max_speed']

        # Check context
        idxs_in = self.check_context('idxs_in', list)
        idxs_out = self.check_context('idxs_out', list)
        trajs = self.check_context('trajs', Trajectories)

        # Just in case the parent didn't do it
        trajs.relabel_fromzero('label', inplace=True)

        # Build matrix
        distances = np.empty((len(trajs.labels),
                              len(trajs.labels)))
        distances.fill(np.nan)
        n = len(idxs_in)
        for i, (idx_in, idx_out) in enumerate(zip(idxs_in, idxs_out)):

            if progress_bar:
                progress = i / n * 100
                print_progress(progress, out=progress_bar_out)

            pos_in = trajs.loc[idx_in]
            pos_out = trajs.loc[idx_out]
            distance = pdist(np.vstack([pos_in[coords].values,
                                        pos_out[coords].values]),
                             metric=distance_metric)
            dt = pos_out.t - pos_in.t
            speed = distance / np.abs(dt)
            if speed < max_speed:
                distances[idx_in[1], idx_out[1]] = distance

        if progress_bar:
            print_progress(-1)

        distances = distances ** 2
        return distances
