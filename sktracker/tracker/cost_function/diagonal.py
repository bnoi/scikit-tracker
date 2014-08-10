
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
from . import AbstractCostFunction

__all__ = ["DiagonalCostFunction"]


class DiagonalCostFunction(AbstractCostFunction):
    """Basic cost function for a diagonal block.

    Parameters
    ----------
    context: `dict`
       this dictionnary must contain at least a `"cost"` key
    parameters: `dict`

    Attributes
    ----------

    context: dict
        Context need to be updated at each `_build` call

        - cost: float
            Default cost

        - objects:
            Vector used to build block matrix

    """

    def __init__(self, context, parameters):
        """
        """

        super(self.__class__, self).__init__(context=context, parameters=parameters)
        self.check_context('cost', float)

    def _build(self):
        """
        """
        objects = self.check_context('objects', object)
        cost = self.check_context('cost', float)

        vect = np.ones(len(objects)) * cost
        mat = self._vector_to_matrix(vect)

        return mat

    def _vector_to_matrix(self, vector):
        """Converts a 1D :class:`numpy.ndarray` to identity 2D :class:`numpy.ndarray`
        with NaNs outside of the diagonal

        Parameters
        ----------
        vector: 1D :class:`numpy.ndarray`

        Returns
        -------
        mat: 2D :class:`numpy.ndarray`
        """

        size = vector.shape[0]
        mat = np.empty((size, size))
        mat[:] = np.nan
        mat[np.diag_indices(size)] = vector

        return mat
