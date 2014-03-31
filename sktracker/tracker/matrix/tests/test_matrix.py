import numpy as np
from numpy.testing import assert_array_equal

from sktracker import data
from sktracker.tracker.matrix import CostMatrix

from sktracker.tracker.cost_function.diagonal import DiagonalCostFunction
from sktracker.tracker.cost_function.brownian import BrownianLinkCostFunction


def nan_ident(size):
    mat = np.identity(size)
    mat[mat == 0] = np.nan
    return mat


def test_cost_matrix_mocked_mat():

    blocks = np.array([[np.ones((1, 2)), np.ones((1, 3)), nan_ident(1), None],
                       [np.ones((3, 2)), None, None, nan_ident(3)],
                       [nan_ident(2), None, None, None],
                       [None, nan_ident(3), None, None]])

    cm = CostMatrix(blocks)
    true_mat = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, np.nan, np.nan,
                np.nan, 1.0, 1.0, np.nan, np.nan, np.nan, np.nan,
                1.0, np.nan, np.nan, 1.0, 1.0, np.nan, np.nan,
                np.nan, np.nan, np.nan, 1.0, np.nan, 1.0, 1.0,
                np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                1.0, 1.0, np.nan, np.nan, np.nan, np.nan, 2.0,
                2.0, 2.0, 2.0, np.nan, 1.0, np.nan, np.nan, np.nan,
                2.0, 2.0, 2.0, 2.0, np.nan, np.nan, 1.0, np.nan,
                np.nan, 2.0, np.nan, np.nan, np.nan, np.nan,
                np.nan, np.nan, 1.0, np.nan, 2.0, np.nan, np.nan,
                np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 2.0,
                np.nan, np.nan, np.nan]

    assert_array_equal(cm.mat.flatten(), true_mat)


def test_cost_matrix_with_mock_trajs():

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[3]
    t1 = times_stamp[4]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    link_cost_func = BrownianLinkCostFunction(parameters={'max_speed': 5.})
    birth_cost_func = DiagonalCostFunction(context={'cost': 5**2.})
    death_cost_func = DiagonalCostFunction(context={'cost': 5**2.})

    link_cost_func.context['pos_in'] = pos0
    link_cost_func.context['pos_out'] = pos1

    birth_cost_func.context['objects'] = pos1
    death_cost_func.context['objects'] = pos0

    cost_matrix_structure = [[link_cost_func.get_block(),  death_cost_func.get_block()],
                             [birth_cost_func.get_block(), None]]

    cm = CostMatrix(cost_matrix_structure)
    assert cm.mat.shape == (10, 10)

    cm.solve()

    assert_array_equal(cm.in_links, [3, 4, 1, 0, 2, 8, 7, 9, 5, 6])
    assert_array_equal(cm.out_links, [3, 2, 4, 0, 1, 8, 9, 6, 5, 7])
