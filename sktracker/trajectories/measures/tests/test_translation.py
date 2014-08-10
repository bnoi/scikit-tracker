import numpy as np
import pandas as pd
from sktracker.trajectories import Trajectories
from sktracker.trajectories.measures import translation

from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_almost_equal


def linear_trajs():

    data = np.array([np.linspace(0, 30, 61),
                     np.zeros(61),
                     np.zeros(61),
                     np.linspace(0, 120, 61)])

    index = pd.MultiIndex.from_tuples([(t, i)  for i in range(2) for t in range(61)],
                                      names=('t_stamp', 'label'))

    trajs = pd.DataFrame(
        np.vstack([data.T, data.T]),
        index=index,
        columns=['x', 'y', 'z', 't']).sortlevel(['t_stamp', 'label'])
    return Trajectories(trajs)

def test_cum_disp():

    trajs = linear_trajs()
    c_disp = translation.cum_disp(trajs)
    assert np.all(c_disp.cum_disp == trajs.x)

def test_p2p_cum_dir():

    trajs = linear_trajs()
    p2p_cd = translation.p2p_cum_dir(trajs, t_stamp0=0, t_stamp1=10)
    assert np.all(p2p_cd == 1)


def test_p2p_directionality():

    trajs = linear_trajs()
    p2p_dir = translation.p2p_directionality(trajs, t_stamp0=0, t_stamp1=10)
    assert np.all(p2p_dir == 1)


def test_p2p_processivity():

    trajs = linear_trajs()
    p2p_p = translation.p2p_processivity(trajs, t_stamp0=0, t_stamp1=10)
    assert np.all(p2p_p == 1)


def test_sld_dir():
    trajs = linear_trajs()
    sld_dir = translation.sld_dir(trajs, window=4).dropna()
    assert(np.all(sld_dir['sld_dir'] == 1))


def test_sld_processivity():
    trajs = linear_trajs()
    sld_processivity = translation.sld_processivity(trajs, window=4).dropna()

    assert(np.all(sld_processivity['sld_processivity'] == 1))


def test_sld_cum_dir():
    trajs = linear_trajs()
    sld_cum_dir = translation.sld_cum_dir(trajs, window=4).dropna()
    assert(np.all(sld_cum_dir['sld_cum_dir'] == 1))


def test_get_MSD():
    trajs = linear_trajs()
    msd = translation.get_MSD(trajs)
    assert_array_almost_equal(np.sqrt(msd['MSD']), trajs.x)

