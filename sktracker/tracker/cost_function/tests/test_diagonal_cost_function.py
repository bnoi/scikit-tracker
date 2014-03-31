import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from nose.tools import assert_raises

from sktracker.tracker.cost_function.diagonal import DiagonalCostFunction


def test_diagonals():

    cost_func = DiagonalCostFunction(context={'cost': 1.})

    objects = np.arange(0, 4)
    cost_func.context['objects'] = objects

    block = cost_func.get_block().flatten()

    true_block = [1.0, np.nan, np.nan, np.nan, np.nan, 1.0, np.nan, np.nan,
                  np.nan, np.nan, 1.0, np.nan, np.nan, np.nan, np.nan, 1.0]

    assert_array_almost_equal(block, true_block)
