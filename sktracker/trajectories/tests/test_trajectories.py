
# -*- coding: utf-8 -*-


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


def test_empty():
    empty = Trajectories.empty_trajs(columns=['x', 'y'])

    assert empty.shape == (0, 2)
    assert empty.empty is True


def test_reverse():
    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert trajs.reverse().shape == (25, 5)

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    trajs.reverse(inplace=True)

    assert trajs.shape == (25, 5)


def test_write_hdf():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    tmp_store = tempfile.NamedTemporaryFile(suffix='h5')
    with pd.get_store(tmp_store.name) as store:
        store['trajs'] = trajs


def test_interpolate():

    trajs = Trajectories(data.with_gaps_df())
    trajs.set_index('true_label', inplace=True, append=True)
    trajs.reset_index(level='label', drop=True, inplace=True)
    trajs.index.set_names(['t_stamp', 'label'], inplace=True)
    interpolated = trajs.time_interpolate(sampling=3, time_step=0.1, s=1)
    # t_stamps_in = interpolated.index.get_level_values('t_stamp')
    # indexer = t_stamps_in % 2 == 0
    # interpolated.loc[indexer].shape, trajs.shape
    # indexer = interpolated.t_stamps % 3 == 0
    # assert interpolated.loc[indexer].shape[0] == trajs.shape[0]
    dts = interpolated.get_segments()[0].t.diff().dropna()
    # All time points should be equaly spaced
    assert_almost_equal(dts.min(), dts.max())


def get_get_diff():

    trajs = Trajectories(data.brownian_trajs_df())
    diffs = trajs.get_diff()
    x_diffs = diffs.to_dict()['x']

    real_x_diffs = {(1, 2): 3.8452299074207819,
                    (3, 2): 4.7476193900872765,
                    (0, 0): np.nan,
                    (3, 0): 0.54161236467700746,
                    (0, 4): np.nan,
                    (1, 4): -5.6929349491048624,
                    (1, 3): -30.136494087633611,
                    (2, 3): 23.240228721514185,
                    (2, 1): -23.9264368052234,
                    (2, 4): 0.63465512968445115,
                    (4, 2): -4.5501817884252063,
                    (1, 0): 20.307078207040306,
                    (0, 3): np.nan,
                    (4, 0): -14.421880216023439,
                    (0, 1): np.nan,
                    (3, 3): -6.5845079821965991,
                    (4, 1): -19.329775838349192,
                    (3, 1): 18.084232469105203,
                    (4, 4): 24.644945052453025,
                    (0, 2): np.nan,
                    (2, 0): 5.6292750381105723,
                    (4, 3): 13.209596167161628,
                    (2, 2): -3.7469188310869228,
                    (3, 4): -17.381636024737336,
                    (1, 1): 13.827909766138866}

    assert_almost_equal(x_diffs, real_x_diffs)


def test_get_speeds():

    trajs = Trajectories(data.brownian_trajs_df())
    speeds = trajs.get_speeds().tolist()

    real_speeds = [np.nan,
                   np.nan,
                   np.nan,
                   np.nan,
                   np.nan,
                   857.99153458573994,
                   1596.9530747771976,
                   873.15267834726137,
                   1282.3088174598233,
                   408.98588960526808,
                   378.40023709328955,
                   1809.9895146014187,
                   917.93227668556324,
                   592.31881736181106,
                   0.48325048326444919,
                   0.39551116881922965,
                   798.29858694043128,
                   1085.3214310682606,
                   405.49164945495221,
                   550.37555144616226,
                   1406.707586739079,
                   1031.9444945962532,
                   1077.6619763794718,
                   1445.7789239945778,
                   739.66839622816326]

    assert_almost_equal(speeds, real_speeds)


def test_scale():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    scaled = trajs.scale(factors=[2., 2., 2.],
                         coords=['x', 'y', 'z'], inplace=False)
    assert_array_almost_equal(scaled[['x', 'y', 'z']] / 2., trajs[['x', 'y', 'z']])
    trajs = trajs.scale(factors=[2., 2., 2.],
                        coords=['x', 'y', 'z'], inplace=True)
    assert_array_almost_equal(scaled[['x', 'y', 'z']], trajs[['x', 'y', 'z']])

    assert_raises(ValueError, trajs.scale, factors=[2., 2., 2.], coords=['x', 'y'], inplace=False)


def test_project():

    trajs = Trajectories(data.directed_motion_trajs_df())
    trajs.rename(columns={'true_label': 'new_label'}, inplace=True)
    trajs.relabel()

    trajs.project([0, 1],
                  coords=['x', 'y'],
                  keep_first_time=False,
                  reference=None,
                  inplace=True,
                  progress=False)

    excepted = np.array([[ 0.27027431,  0.        ],
                         [-0.27027431,  0.        ],
                         [-0.25306519,  0.69683713],
                         [ 0.04633664,  0.31722648]])

    assert_array_almost_equal(excepted, trajs.loc[:,['x_proj', 'y_proj']].values[:4])

    trajs = trajs.project([0, 1],
                           coords=['x', 'y'],
                           keep_first_time=False,
                           reference=None,
                           inplace=False,
                           progress=False)

    assert_array_almost_equal(excepted, trajs.loc[:,['x_proj', 'y_proj']].values[:4])

    assert_raises(ValueError, trajs.project, [0, 1], coords=['x', 'y', 'z', 't'])


def test_get_colors():
    """
    """

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    colors = trajs.get_colors()
    assert colors == {0: '#FF0000', 1: '#ADFF00', 2: '#00FFA9', 3: '#0408FF', 4: '#FF00AC'}

    colors = trajs.get_colors(alpha=0.5)
    assert colors == {0: '#FF000080',
                      1: '#ADFF0080',
                      2: '#00FFA980',
                      3: '#0408FF80',
                      4: '#FF00AC80'}

    colors = trajs.get_colors(rgba=True)
    good_colors = {0: (1.0, 0.0, 0.0, 1.0),
                   1: (0.67977809154279767, 1.0, 0.0, 1.0),
                   2: (0.0, 1.0, 0.66360181783683614, 1.0),
                   3: (0.015440535661123769, 0.031618928677752463, 1.0, 1.0),
                   4: (1.0, 0.0, 0.67279469669175529, 1.0)}
    assert colors == good_colors


def test_get_longest_segments():
    """
    """

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert trajs.get_longest_segments(1) == [4]


def test_get_shortest_segments():
    """
    """

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    assert trajs.get_shortest_segments(1) == [0]


def test_remove_segments():
    """
    """

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)

    trajs.remove_segments(1, inplace=True)

    assert np.all(trajs.labels == [0, 2, 3, 4])


def test_merge():
    """
    """

    trajs1 = Trajectories(data.brownian_trajs_df())
    trajs2 = Trajectories(data.brownian_trajs_df())

    new = trajs1.merge(trajs2)

    assert len(trajs1.labels) + len(trajs2.labels) == len(new.labels)


def test_relabel():
    """
    """
    trajs = Trajectories(data.brownian_trajs_df())
    trajs.columns = ['x', 'y', 'z', 'new_label', 't']
    trajs.relabel(inplace=True)

    new_values = [[1.933058243735795, -14.581064591435775, 11.603556633147544, 0.0],
                  [-12.862215173899491, -2.8611502446443238, -2.2738941196781424, 0.0],
                  [9.100887851132633, 2.837252570763561, 2.875753940450461, 0.0],
                  [-9.253860446235523, 11.345550876585719, 22.118203258275745, 0.0]]

    assert trajs.iloc[:4].values.tolist() == new_values

    trajs = Trajectories(data.brownian_trajs_df())
    trajs.columns = ['x', 'y', 'z', 'new_label', 't']
    trajs = trajs.relabel(inplace=False)

    new_values = [[1.933058243735795, -14.581064591435775, 11.603556633147544, 0.0],
                  [-12.862215173899491, -2.8611502446443238, -2.2738941196781424, 0.0],
                  [9.100887851132633, 2.837252570763561, 2.875753940450461, 0.0],
                  [-9.253860446235523, 11.345550876585719, 22.118203258275745, 0.0]]

    assert trajs.iloc[:4].values.tolist() == new_values


def test_relabel_fromzero():
    """
    """

    trajs = Trajectories(data.brownian_trajs_df())
    original_labels = trajs.labels

    trajs.reset_index(inplace=True)
    trajs.loc[:, 'label'][trajs['label'] == 1] = 55
    trajs.set_index(['t_stamp', 'label'], inplace=True)

    relabeled = trajs.relabel_fromzero('label', inplace=False)
    assert np.all(relabeled.labels == original_labels)

    trajs.reset_index(inplace=True)
    trajs.loc[:, 'label'][trajs['label'] == 1] = 55
    trajs.set_index(['t_stamp', 'label'], inplace=True)

    relabeled = trajs.relabel_fromzero('label', inplace=False)
    assert np.all(relabeled.labels == original_labels)


def test_remove_spots():
    """
    """

    trajs = Trajectories(data.brownian_trajs_df())
    new_trajs = trajs.remove_spots([(3, 2), (0, 0)], inplace=False)

    new_indexes = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2),
                   (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                   (3, 0), (3, 1), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2),
                   (4, 3), (4, 4)]

    assert new_trajs.index.tolist() == new_indexes

    new_trajs = trajs.remove_spots((0, 0), inplace=False)

    new_indexes = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2),
                   (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                   (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1),
                   (4, 2), (4, 3), (4, 4)]

    assert new_trajs.index.tolist() == new_indexes


def test_merge_segments():
    """
    """
    trajs = Trajectories(data.brownian_trajs_df())

    trajs.reset_index(inplace=True)
    trajs.loc[15, ['label']] = 88
    trajs.loc[20, ['label']] = 88
    trajs.set_index(['t_stamp', 'label'], inplace=True)

    new_trajs = trajs.merge_segments([0, 88], inplace=False)

    assert_array_equal(trajs.values, new_trajs.values)

    trajs = Trajectories(data.brownian_trajs_df())
    good_trajs = trajs.copy()

    trajs.reset_index(inplace=True)
    trajs.loc[15, ['label']] = 88
    trajs.loc[20, ['label']] = 88
    trajs.set_index(['t_stamp', 'label'], inplace=True)

    trajs.merge_segments([0, 88], inplace=True)

    assert_array_equal(trajs.values, good_trajs.values)


def test_cut_segments():
    """
    """
    trajs = Trajectories(data.brownian_trajs_df())

    trajs.cut_segments((2, 3), inplace=True)

    new_indexes = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1),
                   (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (4, 0),
                   (4, 1), (4, 2), (4, 4), (4, 5)]

    assert trajs.index.tolist() == new_indexes

    trajs = Trajectories(data.brownian_trajs_df())

    trajs = trajs.cut_segments((2, 3), inplace=False)

    new_indexes = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1),
                   (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (4, 0),
                   (4, 1), (4, 2), (4, 4), (4, 5)]

    assert trajs.index.tolist() == new_indexes


def test_duplicate_segments():
    """
    """
    trajs = Trajectories(data.brownian_trajs_df())

    trajs = trajs.duplicate_segments(2)

    new_indexes = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0),
                   (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1),
                   (2, 2), (2, 3), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2),
                   (3, 3), (3, 4), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3),
                   (4, 4), (4, 5)]

    assert trajs.index.tolist() == new_indexes


def test_get_bounds():
    """
    """

    trajs = Trajectories(data.brownian_trajs_df())
    trajs['t'] *= 10
    t_stamp_bounds = {0: (0, 4), 1: (0, 4), 2: (0, 4), 3: (0, 4), 4: (0, 4)}
    t_bounds = {0: (0.0, 40.0), 1: (0.0, 40.0), 2: (0.0, 40.0), 3: (0.0, 40.0), 4: (0.0, 40.0)}

    assert trajs.get_bounds() == t_stamp_bounds
    assert trajs.get_bounds(column='t') == t_bounds


def test_get_t_stamps_correspondences():
    """
    """

    trajs = Trajectories(data.brownian_trajs_df())
    trajs['t'] *= 33
    data_values = [132, 33, 99, 66, 33, 33, 99., 99, 132]
    t_stamps = trajs.get_t_stamps_correspondences(data_values, column='t')

    assert_array_equal(t_stamps, [4, 1, 3, 2, 1, 1, 3, 3, 4])
