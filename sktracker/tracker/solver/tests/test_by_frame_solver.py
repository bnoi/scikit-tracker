import io

from sktracker import data
from sktracker.tracker.solver import ByFrameSolver
from sktracker.tracker.utils import get_scores_on_trajectories


def test_by_frame_solver():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 1


def test_by_frame_solver_with_bad_parameters():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=0)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 0.2


def test_by_frame_solver_progress_bar():

    true_trajs = data.brownian_trajs_df()

    out = io.StringIO()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5)
    solver.track(progress_bar=True, progress_bar_out=out)

    real_bar = out.getvalue().replace(" ", "").replace("=", "")
    bar = '\r0%[>]t_in:0|t_out1\r25%[>]t_in:1|t_out2\r50%[>]t_in:2|t_out3\r75%[>]t_in:3|t_out4'

    assert bar == real_bar
