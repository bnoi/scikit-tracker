from sktracker.tracker.solver import GapCloseSolver
from sktracker import data


def test_gap_close_get_candidates():

    trajs = data.with_gaps_df()
    max_speed = 10.
    maximum_gap = 5
    gc_solver = GapCloseSolver.for_brownian_motion(trajs,
                                                   max_speed=max_speed,
                                                   maximum_gap=maximum_gap)
    in_idxs, out_idxs = gc_solver._get_candidates()

    for in_idx, out_idx in zip(in_idxs, out_idxs):
        dt = out_idx[0] - in_idx[0]
        assert 0 < dt < maximum_gap
    
def test_gap_close():

    trajs = data.with_gaps_df()
    max_speed = 10.
    maximum_gap = 5
    gc_solver = GapCloseSolver.for_brownian_motion(trajs,
                                                   max_speed=max_speed,
                                                   maximum_gap=maximum_gap)
    gc_solver.track()

    seg_shapes = [seg[1].shape for seg in gc_solver.trajs.iter_segments]
    assert seg_shapes == [(16, 5), (19, 5), (19, 5), (2, 5)]