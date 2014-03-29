import numpy as np

from sktracker.tracker import matrices
from sktracker import data
from sktracker.tracker.matrices import LinkBlock
from sktracker.tracker.matrices import DiagBlock
from sktracker.tracker.matrices import CostMatrix

from sktracker.tracker.cost_function import AbstractLinkCostFunction
from sktracker.tracker.cost_function import AbstractDiagCostFunction


def nan_ident(size):
    mat = np.identity(size)
    mat[mat == 0] = np.nan
    return mat


def test_cost_matrix_mocked_mat():

    blocks = np.array([[np.ones((1, 2)), np.ones((1, 3)), nan_ident(1), None],
                       [np.ones((3, 2)), None, None, nan_ident(3)],
                       [nan_ident(2), None, None, None],
                       [None, nan_ident(3), None, None]])

    cm = matrices.CostMatrix(blocks)
    true_mat = np.array([[ 1.,   1.,   1.,   1.,   1.,   1.,  np.nan,  np.nan,  np.nan],
                         [ 1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,   1.,  np.nan,  np.nan],
                         [ 1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,   1.,  np.nan],
                         [ 1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,   1.],
                         [ 1.,  np.nan,  np.nan,  np.nan,  np.nan,   2.,   2.,   2.,   2.],
                         [np.nan,   1.,  np.nan,  np.nan,  np.nan,   2.,   2.,   2.,   2.],
                         [np.nan,  np.nan,   1.,  np.nan,  np.nan,   2.,  np.nan,  np.nan,  np.nan],
                         [np.nan,  np.nan,  np.nan,   1.,  np.nan,   2.,  np.nan,  np.nan,  np.nan],
                         [np.nan,  np.nan,  np.nan,  np.nan,   1.,   2.,  np.nan,  np.nan,  np.nan]])

    assert np.all(cm.mat[np.isfinite(cm.mat)] == true_mat[np.isfinite(true_mat)])


def test_cost_matrix_mocked_flat():

    blocks = np.array([[np.ones((1, 2)), np.ones((1, 3)), nan_ident(1), None],
                       [np.ones((3, 2)), None, None, nan_ident(3)],
                       [nan_ident(2), None, None, None],
                       [None, nan_ident(3), None, None]])

    cm = matrices.CostMatrix(blocks)
    tru_in, tru_out, tru_costs = (np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3,
                                            3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
                                            5, 5, 6, 6, 7, 7, 8, 8]),
                                  np.array([0, 1, 2, 3, 4, 5, 0, 1, 6, 0, 1, 7, 0,
                                            1, 8, 0, 5, 6, 7, 8, 1, 5, 6,
                                            7, 8, 2, 5, 3, 5, 4, 5]),
                                  np.array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                                             1.,  1.,  1.,  2.,  2.,  2.,  2.,  1.,  2.,  2.,  2.,  2.,  1.,
                                             2.,  1.,  2.,  1.,  2.]))
    idx_in, idx_out, costs = cm.get_flat()

    assert (np.all(idx_in == tru_in)
            and np.all(idx_out == tru_out)
            and np.all(costs == tru_costs))


def test_cost_matrix_with_mock_trajs():

    trajs = data.directed_trajectories_generator(n_part=5,
                                                 n_times=10,
                                                 noise=1e-10,
                                                 p_disapear=0.4,
                                                 sampling=10,
                                                 seed=0)

    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t_0_vec = times_stamp[:-1]
    t_1_vec = times_stamp[1:]

    for t0, t1 in zip(t_0_vec, t_1_vec):
        pos0 = trajs.ix[t0]
        pos1 = trajs.ix[t1]

        fn = lambda: build_cost_matrix(pos0, pos1)
        fn.description = "Check CostMatrix build is correct for t0 = {} and t1 = {}".format(t0, t1)

        yield fn


def build_cost_matrix(pos0, pos1):

    link_cost_func = AbstractLinkCostFunction(None, {})
    diag_cost_func = AbstractDiagCostFunction(None, {})

    link_block = LinkBlock(pos0, pos1, link_cost_func)
    death_block = DiagBlock(pos0, diag_cost_func)
    birth_block = DiagBlock(pos1, diag_cost_func)

    cost_matrix_structure = [[link_block.mat,  death_block.mat],
                             [birth_block.mat, None]]

    cm = CostMatrix(cost_matrix_structure)

    cost_matrix_shape = (pos0.shape[0] + pos1.shape[0],
                         pos0.shape[0] + pos1.shape[0])

    assert cm.mat.shape == cost_matrix_shape
