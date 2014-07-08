import numpy as np
import pandas as pd
from sktracker.trajectories import Trajectories
from sktracker.trajectories.measures import transformation
from sktracker import data


from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_almost_equal


def test_back_proj_interp():
    trajs = Trajectories(data.with_gaps_df())
    interpolated = transformation.time_interpolate(trajs,
                                                   sampling=3, s=0)
    back_proj = transformation.back_proj_interp(interpolated, trajs, 3)
    assert_almost_equal(back_proj.iloc[0].x, trajs.iloc[0].x)

    interpolated = transformation.time_interpolate(trajs,
                                                   sampling=3, s=2)
    back_proj = transformation.back_proj_interp(interpolated, trajs, 3)
    assert_almost_equal(back_proj.iloc[0].x, trajs.iloc[0].x)


def test_back_proj_pca():

    trajs = Trajectories(data.with_gaps_df())
    rotated, pca = transformation.do_pca(trajs, suffix='',
                                         append=False, return_pca=True)
    back_proj = transformation.back_proj_pca(rotated, pca, coords=['x', 'y', 'z'])
    assert_almost_equal(back_proj.iloc[0].x, trajs.iloc[0].x)
