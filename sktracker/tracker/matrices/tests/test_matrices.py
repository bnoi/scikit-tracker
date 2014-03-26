import numpy as np
from sktracker.tracker import matrices



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
    true_mat = np.array([[  1.,   1.,   1.,   1.,   1.,   1.,  np.nan,  np.nan,  np.nan],
                         [  1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,   1.,  np.nan,  np.nan],
                         [  1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,   1.,  np.nan],
                         [  1.,   1.,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,  np.nan,   1.],
                         [  1.,  np.nan,  np.nan,  np.nan,  np.nan,   2.,   2.,   2.,   2.],
                         [ np.nan,   1.,  np.nan,  np.nan,  np.nan,   2.,   2.,   2.,   2.],
                         [ np.nan,  np.nan,   1.,  np.nan,  np.nan,   2.,  np.nan,  np.nan,  np.nan],
                         [ np.nan,  np.nan,  np.nan,   1.,  np.nan,   2.,  np.nan,  np.nan,  np.nan],
                         [ np.nan,  np.nan,  np.nan,  np.nan,   1.,   2.,  np.nan,  np.nan,  np.nan]])
    assert  np.all(cm.mat[np.isfinite(cm.mat)] == true_mat[np.isfinite(true_mat)])

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
