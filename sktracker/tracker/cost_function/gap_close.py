
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from . import AbstractCostFunction

__all__ = ["AbstractGapCloseCostFunction"]


class AbstractGapCloseCostFunction(AbstractCostFunction):
    """
    """

    def __init__(self, context, parameters):
        """
        """
        super(AbstractGapCloseCostFunction, self).__init__(context=context, parameters=parameters)

    def check_idxs_length(self):
        """Check wether idxs_in and idxs_out have the same length.
        """

        idxs_in = self.check_context('idxs_in', list)
        idxs_out = self.check_context('idxs_out', list)

        if not len(idxs_in) == len(idxs_out):
            raise ValueError('''self.context['idxs_in'] and self.context['idxs_out']
                             must have the same length ''')
