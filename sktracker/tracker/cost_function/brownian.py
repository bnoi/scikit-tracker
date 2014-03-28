import numpy as np
from scipy.spatial.distance import cdist
from . import AbstractLinkCostFunction


class BrownianCostFunction(AbstractLinkCostFunction):
    """This class generates cost matrices for brownian motion
    trajectories.

    The cost between two position is given by the square of their
    distance

    Attributes
    ----------

    paramters: a `dict`
        used by the `build` method, with the following keys:
        * 'distance_metric': a string, default 'euclidean',
          passed to `scipy.spatial.distance.cdist`
          (see this function documentation for more)

        * 'coords': a list of column names on which to compute the distance,
            default ['x', 'y', 'z']
        * 'max_speed': a float, default 1. All the values of the cost matrix
           for which the distance *divided by the time difference* is higher than
           this parameter's value are set to np.nan

    """

    def __init__(self, parameters):

        _parameters = {'distance_metric': 'euclidean',
                       'max_speed': 1.,
                       'coords': ['x', 'y', 'z']}
        _parameters.update(parameters)
        super().__init__({}, _parameters)

    def build(self, pos_in, pos_out):
        """
        Computes and returns the cost matrix between pos_in and pos_out.

        Parameters
        ----------

        pos_in: a :class:`pandas.DataFrame`
            The object coordinates to link from

        pos_out: a :class:`pandas.DataFrame`
            The object coordinates to link to

        Notes
        -----

        Both arguments must contain the columns listed in `self.parameters['coords']`
        plus one column named 't' containing the time position of each objects.
        """
        coords = self.parameters['coords']
        distance_metric = self.parameters['distance_metric']
        max_speed = self.parameters['max_speed']

        self.check_columns([pos_in, pos_out], list(coords)+['t'])

        distances = cdist(pos_in[coords].astype(np.float),
                          pos_out[coords].astype(np.float),
                          metric=distance_metric)

        dt = pos_out['t'].iloc[0] - pos_in['t'].iloc[0]

        distances /= np.abs(dt)
        distances[distances > max_speed] = np.nan
        return distances ** 2
