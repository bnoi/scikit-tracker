from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_almost_equal

import numpy as np
import pandas as pd

from sktracker.trajectories import Trajectories
from sktracker.trajectories.measures import transformation
from sktracker import data
from sktracker.trajectories.measures.transformation import transformations_matrix
from sktracker.trajectories.measures.transformation import interp_series


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


def test_transformations_matrix():

    A = transformations_matrix([0, 0], [1, 0])
    excepted = np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

    assert_array_almost_equal(A, excepted)

    A = transformations_matrix([3, 6], [1, 1])
    excepted = np.array([[0.70710678, -0.70710678, 0],
                         [0.70710678, 0.70710678, 0],
                         [-6.36396103, -2.12132034, 1]])

    assert_array_almost_equal(A, excepted)


def test_interp_series():

    series = pd.Series([0, 10, 20, 40, 50, 60], index=[0, 1, 2, 4, 5, 6])
    new_index = np.arange(0.5, 7.5, 1)
    inter = interp_series(series, new_index)

    assert_array_equal(inter.values, np.array([5, 15, 25, 35, 45, 55, 60]))
