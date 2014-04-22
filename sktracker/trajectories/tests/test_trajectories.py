
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from nose.tools import assert_raises
from nose.tools import assert_dict_equal
from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_almost_equal


import numpy as np
import tempfile
import pandas as pd

from sktracker import data
from sktracker.trajectories import Trajectories


def test_constructor_fail():

    assert_raises(TypeError, Trajectories, "hello")


def test_attributes():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert_array_equal(trajs.t_stamps, np.array([0, 1, 2, 3, 4]))

    assert_array_equal(trajs.labels, np.array([0, 1, 2, 3, 4]))

    segments = {0: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
                1: [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
                2: [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],
                3: [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)],
                4: [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]}
    assert_dict_equal(trajs.segment_idxs, segments)

    traj = np.array([[ -9.25386045,  11.34555088,  22.11820326,   3.        ,   0.        ],
                     [ 11.05321776,   3.23738477,   2.62790435,   2.        ,   1.        ],
                     [ 16.6824928 ,  14.602054  , -12.1218683 ,   4.        ,   2.        ],
                     [ 17.22410516,  14.8068125 , -11.87642753,   4.        ,   3.        ],
                     [  2.80222495, -13.13783042,   8.56406878,   0.        ,   4.        ]])
    t_stamp, traj_to_test = list(trajs.iter_segments)[0]
    assert_array_almost_equal(traj, traj_to_test)

    assert list(trajs.get_segments().keys()) == [0, 1, 2, 3, 4]


def test_structure():
    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert_raises(ValueError, trajs.check_trajs_df_structure, ['t_idx'])
    assert_raises(ValueError, trajs.check_trajs_df_structure, ['t_stamp', 'label'], ['dx'])

    trajs.check_trajs_df_structure(['t_stamp', 'label'], ['x', 'y', 'z'])


def test_copy():
    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert isinstance(trajs.copy(), Trajectories)


def test_reverse():
    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert trajs.reverse().shape == (25, 5)


def test_write_hdf():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    tmp_store = tempfile.NamedTemporaryFile(suffix='h5')
    with pd.get_store(tmp_store.name) as store:
        store['trajs'] = trajs


def get_mean_dist():

    true_trajs = data.brownian_trajs_df()

    trajs = Trajectories(true_trajs)
    mean_dist = trajs.get_mean_distances()

    true_dist = np.array([1.58959148, 1.42974187,
                          1.97505829, 1.93212297, 1.30778342])

    assert_array_almost_equal(true_dist, mean_dist.values.flatten())


def test_interpolate():

    trajs = Trajectories(data.with_gaps_df())
    trajs.set_index('true_label', inplace=True, append=True)
    trajs.reset_index(level='label', drop=True, inplace=True)
    trajs.index.set_names(['t_stamp', 'label'], inplace=True)
    interpo = trajs.time_interpolate(time_step=0.1, s=1)
    dts = interpo.get_segments()[0].t.diff().dropna()
    ## All time points should be equaly spaced
    assert_almost_equal(dts.min(), dts.max())