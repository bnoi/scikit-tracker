from sktracker import data
from sktracker.tracker.solver import ByFrameSolver
from sktracker.tracker.utils import get_scores_on_trajectories


def test_byframe_solver():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 1 and conserved_trajectories_number == 1


def test_byframe_solver_with_bad_parameters():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=0)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 1 and conserved_trajectories_number == 0.2
