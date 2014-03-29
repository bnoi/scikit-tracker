import numpy as np

from ..cost_function import AbstractLinkCostFunction
from ..cost_function import AbstractDiagCostFunction

__all__ = []


class Block():
    """A matrix block.
    """
    pass


class LinkBlock(Block):
    """LinkBlock are built with two vectors.

    Parameters
    ----------
    objects_in : 1D array of :class:`pandas.DataFrame`
        To fill Y block axis.
    objects_out : 1D array of :class:`pandas.DataFrame`
        To fill X block axis.
    cost_function : :class:`sktracker.tracker.cost_function.AbstractCostFunction`
        Used to compute block costs.

    """

    def __init__(self,
                 objects_in,
                 objects_out,
                 cost_function):

        self.objects_in = objects_in
        self.objects_out = objects_out

        if not isinstance(cost_function, AbstractLinkCostFunction):
            raise TypeError("cost_function needs to inherit from "
                            "sktracker.tracker.cost_function.AbstractLinkCostFunction")
        self.cost_function = cost_function
        self.mat = None

        self._build()

    def _build(self):
        """Compute and built block.
        """

        self.mat = self.cost_function.build(self.objects_in, self.objects_out)

        if self.mat.shape != (len(self.objects_in),
                              len(self.objects_out)):
            self.mat = None
            raise ValueError('Cost_function does not returns'
                             ' a correct cost matrix')


class DiagBlock(Block):
    """DiagBlock are built with one single vector. It is an identity matrix.

    Parameters
    ----------
    objects : 1D array of :class:`pandas.DataFrame`
        To fill the identity matrix.
    cost_function : :class:`sktracker.tracker.CostFunction`
        Used to compute block costs.

    """
    def __init__(self, objects, cost_function):

        self.objects = objects

        if not isinstance(cost_function, AbstractDiagCostFunction):
            raise TypeError("cost_function needs to inherit from "
                            "sktracker.tracker.cost_function.DiagCostFunction")

        self.cost_function = cost_function
        self.vect = None
        self.mat = None
        self._build()

    def _build(self):
        """Compute and built block.
        """
        self.vect = self.cost_function.build(self.objects)

        if self.vect.size != len(self.objects):
            self.mat = None
            self.vect = None
            raise ValueError('cost_function does not returns'
                             ' a correct cost vector')

        self._get_matrix()

    def _get_matrix(self):
        """Get matrix and replace 0 values with `numpy.nan`.
        """

        size = self.vect.shape[0]
        self.mat = np.empty((size, size))
        self.mat[:] = np.nan
        self.mat[np.diag_indices(size)] = self.vect
