
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import io

import numpy as np

from sktracker import data
from sktracker.tracker.solver import ByFrameSolver
from sktracker.tracker.utils import get_scores_on_trajectories


def test_by_frame_solver():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5, penalty=2.)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 1


def test_by_frame_solver_with_missing_data():

    true_trajs = data.with_gaps_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5, penalty=2.)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 3 / 7.


def test_by_frame_solver_with_bad_parameters():

    true_trajs = data.brownian_trajs_df()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=0)
    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 0.2


def test_by_frame_solver_progress_bar():

    true_trajs = data.brownian_trajs_df()

    out = io.StringIO()

    solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=5, penalty=2.)
    solver.track(progress_bar=True, progress_bar_out=out)

    real_bar = out.getvalue().replace(" ", "").replace("=", "")
    bar = '\r0%[>]t_in:0|t_out1\r25%[>]t_in:1|t_out2\r50%[>]t_in:2|t_out3\r75%[>]t_in:3|t_out4'

    assert bar == real_bar


def test_for_directed_motion():
    parameters = {'max_speed': 2,
                  'past_traj_time': 5,
                  'smooth_factor': 0,
                  'interpolation_order': 1,
                  'coords': ['x', 'y', 'z'],
                  'penalty': 1.05}

    true_trajs = data.directed_motion_trajs_df()
    solver = ByFrameSolver.for_directed_motion(true_trajs, **parameters)
    trajs = solver.track(progress_bar=True)

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert np.round(min_chi_square, 2) == 0.66 and conserved_trajectories_number == 1
