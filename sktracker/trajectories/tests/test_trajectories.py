
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


def test_write_hdf():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    tmp_store = tempfile.NamedTemporaryFile(suffix='h5')
    with pd.get_store(tmp_store.name) as store:
        store['trajs'] = trajs


def test_get_mean_dist():

    true_trajs = data.brownian_trajs_df()

    trajs = Trajectories(true_trajs)
    mean_dist = trajs.get_mean_distances()

    true_dist = np.array([21.71975058, 35.72098449, 31.40463335, 29.5767909, 17.89387283])

    assert_array_almost_equal(true_dist, mean_dist.values.flatten())


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


def test_all_speeds():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    speeds = trajs.all_speeds()

    real_speeds = [29.29149253,  42.24278092,   1.24544591,  28.5496605 ,
                   31.5956165 ,  21.93710968,  39.96189529,  30.506188  ,
                   23.63875175,   2.02299763,  25.16282357,  34.9177922 ,
                   29.54915698,   0.77486359,  23.92966393,  18.10192901,
                   1.4519421 ,  42.6697699 ,  35.80933981,  38.35867461,
                   2.00826474,  20.00524827,  28.63076735,  23.96234609,
                   20.22339956,  19.45251236,  29.61463181,  25.36724868,
                   1.61745084,  21.17778688,   1.00431235,  42.54397154,
                   35.15677816,  19.85153065,  39.07826864,  43.91553261,
                   1.14867379,  30.29739719,  29.36707721,  32.13200073,
                   36.47041249,  30.15276245,   1.131474  ,  24.3376009 ,
                   24.77755792,  39.50921192,  32.31300005,  23.67070283,
                   20.12833613,   0.6951622 ,   0.62889679,  19.35806068,
                   45.24644565,  39.42756814,  37.55238742,  43.4886719 ,
                   28.25417822,   2.40067016,  32.46583113,  31.23535934,
                   36.41432396,  24.7943914 ,  32.94421696,  23.2506553 ,
                   2.06057683,  20.47042796,   2.22746757,  30.79769909,
                   20.13682322,  24.742422  ,  39.65555878,  21.87756577,
                   33.5356576 ,   1.20844778,  23.46008422,  37.50610066,
                   46.73647432,  38.31748506,   2.14598242,  20.37801735,
                   19.87613565,  32.12389289,  25.36581069,  17.50636222,
                   2.04705   ,  32.53990188,   2.933702  ,  32.82776228,
                   43.24067854,  29.9153449 ,   2.43175831,  36.47559589,
                   20.77942458,  38.02339969,  21.63794875,  20.69995033,
                   35.15221208,   1.75205306,  36.63872024,  27.19684534]

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

    excepted = np.array([[-2.70274309e-01,  0.00000000e+00],
                         [ 2.70274309e-01, -5.55111512e-17],
                         [ 2.53065189e-01, -6.96837132e-01],
                         [-4.63366354e-02, -3.17226478e-01],
                         [-2.11960632e-01,  7.99839159e-02],
                         [ 2.11960632e-01, -7.99839159e-02],
                         [ 2.78304909e-01, -6.09550094e-01],
                         [-5.34263659e-02, -1.91504925e-01],
                         [-1.58343578e-01,  2.35157260e-01],
                         [ 1.58343578e-01, -2.35157260e-01],
                         [ 1.33579973e-01, -5.75121334e-01],
                         [-1.23065020e-01, -7.00631576e-02],
                         [ 8.97266489e-03,  3.52553866e-01],
                         [-8.97266489e-03, -3.52553866e-01],
                         [-4.64718526e-02, -4.83864183e-01],
                         [-4.45522391e-02,  1.28641191e-02],
                         [ 1.53606261e-01,  4.13899744e-01],
                         [-1.53606261e-01, -4.13899744e-01],
                         [ 2.38961153e-02, -3.98748400e-01],
                         [ 1.02108498e-01,  5.99558645e-03],
                         [ 3.31262853e-01,  4.05475741e-01],
                         [-3.31262853e-01, -4.05475741e-01],
                         [ 9.99225313e-02, -2.73583029e-01],
                         [ 2.09043995e-01,  1.82105681e-01],
                         [ 4.15114677e-01,  4.94167333e-01],
                         [-4.15114677e-01, -4.94167333e-01],
                         [ 1.81595719e-01, -3.03742564e-01],
                         [ 2.87850754e-01,  1.32934815e-01],
                         [ 6.35702519e-01,  4.64592079e-01],
                         [-6.35702519e-01, -4.64592079e-01],
                         [ 2.81387768e-01, -2.86210529e-01],
                         [ 4.37014198e-01,  2.01436630e-01],
                         [ 7.44430931e-01,  4.27121995e-01],
                         [-7.44430931e-01, -4.27121995e-01],
                         [ 3.48146051e-01, -2.66836192e-01],
                         [ 5.48097902e-01,  1.72077163e-01],
                         [ 8.93953060e-01,  4.17075988e-01],
                         [-8.93953060e-01, -4.17075988e-01],
                         [ 5.20051609e-01, -2.77121638e-01],
                         [ 7.25346979e-01,  1.77848529e-01]])

    assert_array_almost_equal(excepted, trajs.loc[:,['x_proj', 'y_proj']].values)


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
