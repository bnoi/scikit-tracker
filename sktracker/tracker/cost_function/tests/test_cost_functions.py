import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from nose.tools import assert_raises

from sktracker import data
from sktracker.tracker.matrix import LinkBlock
from sktracker.tracker.matrix import DiagBlock
from sktracker.tracker.matrix import CostMatrix

from sktracker.tracker.cost_function.brownian import BrownianCostFunction
from sktracker.tracker.cost_function import DiagCostFunction


def test_brownian_case():

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[0]
    t1 = times_stamp[1]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    link_cost_func = BrownianCostFunction({'max_speed': 5.})
    diag_cost_func = DiagCostFunction({'cost': 10.})

    link_block = LinkBlock(pos0, pos1, link_cost_func)
    death_block = DiagBlock(pos0, diag_cost_func)
    birth_block = DiagBlock(pos1, diag_cost_func)

    cost_matrix_structure = [[link_block.mat, death_block.mat],
                             [birth_block.mat, None]]

    cm = CostMatrix(cost_matrix_structure)

    a = np.array([1.55113551, 10., 4.09251942, 10.,
                  0.60041359, 10., 2.10813587, 10.,
                  4.03312728, 10., 10., 11.,
                  10., 11., 10., 11.,
                  10., 11., 10., 11.])
    b = np.ma.masked_invalid(cm.mat).compressed()
    assert_array_almost_equal(a, b, decimal=3)


def test_brownian_case_solve_lapjv():

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[0]
    t1 = times_stamp[1]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    link_cost_func = BrownianCostFunction({'max_speed': 5.})
    diag_cost_func = DiagCostFunction({'cost': 10.})

    link_block = LinkBlock(pos0, pos1, link_cost_func)
    death_block = DiagBlock(pos0, diag_cost_func)
    birth_block = DiagBlock(pos1, diag_cost_func)

    cost_matrix_structure = [[link_block.mat, death_block.mat],
                             [birth_block.mat, None]]

    cm = CostMatrix(cost_matrix_structure)

    cm.solve()

    assert_array_equal(cm.in_links, np.array([2, 4, 3, 1, 0, 9, 8, 5, 7, 6]))
    assert_array_equal(cm.out_links, np.array([4, 3, 0, 2, 1, 7, 9, 8, 6, 5]))


def test_abstract_cost_function_check_context():

    c_func = DiagCostFunction({'cost': 1})

    assert_raises(ValueError, c_func.check_context, 'test_string', str)

    c_func.context['test_string'] = 5

    assert_raises(TypeError, c_func.check_context, 'test_string', str)

    c_func.context['test_string'] = "i am a string"
    c_func.check_context('test_string', str)

    assert True
