
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from sktracker.tracker.solver import GapCloseSolver
from sktracker import data


def test_gap_close_get_candidates():

    trajs = data.with_gaps_df()
    max_speed = 10.
    maximum_gap = 5
    gc_solver = GapCloseSolver.for_brownian_motion(trajs,
                                                   max_speed=max_speed,
                                                   maximum_gap=maximum_gap,
                                                   use_t_stamp=True)
    in_idxs, out_idxs = gc_solver._get_candidates()

    assert in_idxs == [(3, 0), (3, 0), (5, 1), (13, 2), (13, 2), (16, 3)]
    assert out_idxs == [(5, 3), (7, 4), (7, 4), (15, 5), (18, 6), (18, 6)]


def test_gap_close_get_candidates_with_t():

    trajs = data.with_gaps_df()
    trajs['t'] *= 10
    max_speed = 10.
    maximum_gap = 50
    gc_solver = GapCloseSolver.for_brownian_motion(trajs,
                                                   max_speed=max_speed,
                                                   maximum_gap=maximum_gap,
                                                   use_t_stamp=False)
    in_idxs, out_idxs = gc_solver._get_candidates()

    assert in_idxs == [(3, 0), (3, 0), (5, 1), (13, 2), (13, 2), (16, 3)]
    assert out_idxs == [(5, 3), (7, 4), (7, 4), (15, 5), (18, 6), (18, 6)]


def test_gap_close():

    trajs = data.with_gaps_df()
    max_speed = 10.
    maximum_gap = 5
    gc_solver = GapCloseSolver.for_brownian_motion(trajs,
                                                   max_speed=max_speed,
                                                   maximum_gap=maximum_gap,
                                                   use_t_stamp=True)
    gc_solver.track()

    seg_shapes = [seg[1].shape for seg in gc_solver.trajs.iter_segments]
    assert seg_shapes == [(18, 5), (19, 5), (19, 5)]
