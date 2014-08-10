# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_almost_equal


from sktracker.trajectories.measures import rotation
from sktracker.trajectories import Trajectories
from sktracker import data


def test_radial_speed():
    trajs = Trajectories(data.with_gaps_df())
    trajs.reset_index(level='label', drop=True, inplace=True)
    trajs.set_index('true_label', drop=True, append=True, inplace=True)
    trajs.index.set_names(['t_stamp', 'label'], inplace=True)
    rd_speeds = rotation.radial_speed(trajs, in_coords=['x', 'y'], from_polar=False)


def test_polar_coords():

    trajs = data.brownian_trajs_df()
    trajs = Trajectories(trajs)
    polar = rotation.get_polar_coords(trajs, get_dtheta=True)
    assert_array_almost_equal(trajs.x, polar.rho * np.cos(polar.theta))


def test_continuous_theta_1d():

    thetas_in = np.array([0, np.pi/2, np.pi, -np.pi/2])
    thetas_out, dthetas = rotation._continuous_theta(thetas_in,
                                                     return_dtheta=True)
    dthetas_th = np.array([np.pi/2, np.pi/2, np.pi/2])
    thetas_th = np.array([0, np.pi/2, np.pi,  3*np.pi/2])
    assert_array_almost_equal(dthetas, dthetas_th)
    assert_array_almost_equal(thetas_out, thetas_th)


def test_continuous_theta_2d():
    thetas_th = np.vstack([np.linspace(0, 2*np.pi, 10),
                           np.linspace(0, 3*np.pi, 10)])

    cos_th = np.cos(thetas_th)
    sin_th = np.sin(thetas_th)

    thetas_in = np.arctan2(sin_th, cos_th)
    thetas_out, dthetas = rotation._continuous_theta(thetas_in,return_dtheta=True)
    thetas_out2, dthetas2 = rotation._continuous_theta(thetas_in.T,
                                                       return_dtheta=True, axis=0)

    assert_almost_equal(thetas_out, thetas_th)
    assert_almost_equal(thetas_out2, thetas_th.T)
