from sktracker.tracker.solver import GapCloseSolver
from sktracker import data


def test_gap_close_solver():

    trajs = data.brownian_trajs_df()
    solver = GapCloseSolver(trajs, 5, None)

    assert solver is not None
