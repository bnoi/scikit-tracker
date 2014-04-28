
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
from numpy.testing import assert_array_almost_equal

from sktracker.tracker.cost_function.diagonal import DiagonalCostFunction


def test_diagonals():

    cost_func = DiagonalCostFunction(context={'cost': 1.},
                                     parameters={'penalty':1.05})

    objects = np.arange(0, 4)
    cost_func.context['objects'] = objects
    cost_func.get_block()
    block = cost_func.mat.flatten()

    true_block = [1.0, np.nan, np.nan, np.nan, np.nan, 1.0, np.nan, np.nan,
                  np.nan, np.nan, 1.0, np.nan, np.nan, np.nan, np.nan, 1.0]

    assert_array_almost_equal(block, true_block)
