from sktracker.tracker.solver import GapCloseSolver
from sktracker import data


def test_gap_close_get_candidates():

    seg_idxs = [[(t, lbl) for lbl in range(5)]

# def test_gap_close_solver():

#     trajs = data.brownian_trajs_df()
#     solver = GapCloseSolver(trajs, None, 5)

#     assert solver is not None
