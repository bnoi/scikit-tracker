# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pandas as pd
from ..trajectories import Trajectories

from .measure_decorators import trajs_measure

import logging
log = logging.getLogger(__name__)


def dir_shift_(segment, shift=1, coords=['v_x', 'v_y', 'v_z']):

    cross = np.cross(segment[coords].shift(-shift//2),
                     segment[coords].shift(shift//2+1), axis=-1)
    norm = np.linalg.norm(segment[coords].shift(shift//2+1), axis=1)
    norm_s = np.linalg.norm(segment[coords].shift(-shift//2), axis=1)
    #data = np.linalg.norm(cross, axis=1) / (norm * norm_s)
    data = cross[:, -1] / (norm * norm_s)
    df = pd.DataFrame(np.arcsin(data), index=segment.index)
    return df


@trajs_measure
def dir_shift(trajs, shift=1, coords=['v_x', 'v_y', 'v_z']):
    """
    """
    gp = trajs.groupby(level=['label'], group_keys=False)
    return gp.apply(dir_shift_, shift=shift, coords=coords)


# Trajectories pseudo methods

def radial_speed(trajs, in_coords=['rho', 'theta'],
                 from_polar=True,
                 smooth=0,
                 append=False,
                 out_coords=['v_rad', 'v_orad', 'v_theta']):
    """
    """
    if not from_polar:
        polar = get_polar_coords(trajs, get_dtheta=False,
                                 in_coords=in_coords,
                                 out_coords=['rho', 'theta'],
                                 periodic=False, append=False)
        in_coords = ['rho', 'theta']
    else:
        polar = trajs[in_coords].copy()

    polar = Trajectories(polar)
    polar['t'] = trajs['t']
    intp_polar = polar.time_interpolate(coords=['rho', 'theta'], s=smooth, k=3)
    radial_speed_c, ortho_rad_speed_c, angular_speed_c = out_coords
    radial_speed = intp_polar['v_rho']
    ortho_rad_speed = intp_polar['rho'] * intp_polar['v_theta']
    angular_speed = intp_polar['v_theta']
    speeds = pd.DataFrame.from_dict({radial_speed_c: radial_speed,
                                     ortho_rad_speed_c: ortho_rad_speed,
                                     angular_speed_c: angular_speed})
    speeds.set_index(intp_polar.index)
    speeds = speeds.loc[trajs.index]
    speeds['t'] = trajs.t
    if append:
        for coord in speeds.columns:
            trajs[coord] = speeds[coord]
        return trajs

    return speeds


def get_polar_coords(trajs, get_dtheta=False,
                     in_coords=['x', 'y'],
                     out_coords=['rho', 'theta'],
                     periodic=False, append=False):
    '''Computes the polar coordinates for trajectories
    from the cartesian coordinates given by in_coords.

    Let :math:`x` and :math:`y` be the input coordinates, it will compute
    :math:`\theta = tan^{-1}(y/x)` and :math:`rho = \sqrt{x^2+y^2}`

    Parameters
    ----------
    trajs : :class:`Trajectories` instance
    get_dtheta : bool, default False
        if True, will also compute the angular shift between two successive points
        for each segment of the trajectories. This angular shift is corrected
        for periodic boundary conditions and defined in :math:`[-\pi, \pi]`
    in_coords : list of two strings, default ['x', 'y']
        the coordinates used to compute the angle and radius
    out_coords : list of strings, default ['rho', 'theta']
        the coordinates as which the angle and radius will be named (in this order!)
    periodic : bool, default False
        if True, simply use arctan2 and returns angles in :math:`[-\pi, \pi]`
        if False, the returned angles are continuous for each segment
    append : bool, default False
        if True, appends the computed columns to the input trajectories and return them
        if Fase, only returns the computed columns
    '''

    if len(in_coords) != 2:
        raise ValueError('''Only valid for two input coordinates''')
    x_coord, y_coord = in_coords
    rho_coord, theta_coord = out_coords
    thetas = np.arctan2(trajs[y_coord], trajs[x_coord])
    rhos = np.hypot(trajs[y_coord], trajs[x_coord])
    polar_trajs = pd.DataFrame.from_dict({theta_coord: thetas,
                                          rho_coord: rhos})
    polar_trajs.set_index(trajs.index, inplace=True)
    polar_trajs['t'] = trajs.t
    if not periodic:
        polar_trajs = polar_trajs.groupby(level='label').apply(continuous_theta_,
                                                               theta_coord, get_dtheta)
    elif get_dtheta:
        polar_trajs = polar_trajs.groupby(
            level='label').apply(periodic_dtheta_,
                                 theta_coord)
    polar_trajs = polar_trajs.sortlevel(['t_stamp', 'label'])
    if append:
        for coord in polar_trajs.columns:
            trajs[coord] = polar_trajs[coord]
        return trajs
    return polar_trajs


def get_spherical_coords(trajs, get_dtheta=False,
                         in_coords=['x', 'y', 'z'],
                         out_coords=['r', 'theta', 'phi'],
                         periodic=False,
                         append=False):
    """
    """

    x, y, z = in_coords
    r, theta, phi = out_coords
    thetas = np.arctan2(trajs[y], trajs[x])
    rs = np.linalg.norm(trajs[in_coords], axis=1)
    phis = np.arccos(trajs[z]/rs)
    spherical_trajs = pd.DataFrame.from_dict({r: rs,
                                              theta: thetas,
                                              phi: phis})

    if not periodic:
        spherical_trajs = spherical_trajs.groupby(
            level='label').apply(continuous_theta_,
                                 theta, get_dtheta=get_dtheta)
        spherical_trajs = spherical_trajs.groupby(
            level='label').apply(continuous_theta_,
                                 phi, get_dtheta=get_dtheta)

    return spherical_trajs.sortlevel(['t_stamp', 'label'])

# Segment method


def continuous_theta_(segment, coord='theta', get_dtheta=True):
    """
    """

    out = _continuous_theta(segment[coord].values,
                            return_dtheta=get_dtheta)
    if get_dtheta:
        thetas, dthetas_ = out
        dthetas = np.zeros_like(thetas)
        dthetas[1:] = dthetas_
        segment['d'+coord] = dthetas
        segment[coord] = thetas
    else:
        segment[coord] = out
    return segment


def periodic_dtheta_(segment, coord='theta'):
    dtheta_ = np.zeros_like(segment[coord].values).ravel()
    dtheta_[1:] = _periodic_dtheta(segment[coord].values)
    segment['d'+coord] = dtheta_
    return segment

# Array methods


def _continuous_theta(thetas, return_dtheta=True, axis=-1):
    '''Shifts the passed angles by multiples of ::math:2\np.pi such that
    the result is continuous (i.e. accumulating circles).

    If `return_dtheta` is True, also returns the difference between
    two consecutive values, corrected for periodic boundary conditions
    between ::math:\pi: and ::math:-\pi:

    Parameters
    ----------
    thetas : ndarray, angle vaues in radians
    return_dtheta : bool, default True

    Returns :
    ---------
    thetas : ndarray, corrected angle values
    dthetas : ndarray, pbc corrected angle differences

    '''
    thetas = np.atleast_1d(thetas)
    if thetas.size == 1:
        if return_dtheta:
            return thetas, None
        else:
            return thetas
    if thetas.ndim == 1:
        return _1d_continuous_thetas(thetas, return_dtheta)

    thetas_out = np.apply_along_axis(_1d_continuous_thetas,
                                     axis, thetas, False)
    if not return_dtheta:
        return thetas_out
    else:
        ### Here we have to compute the diff again
        ### I don't really know how to avoid this
        return thetas_out, np.diff(thetas_out, axis=axis)


def _periodic_dtheta(thetas, axis=-1):
    '''Returns  the difference between
    two consecutive angles, corrected for periodic boundary conditions
    between ::math:\pi and ::math:-\pi

    Parameters
    ----------
    thetas : ndarray, angle vaues in radians
    axis : int, default -1
        the axis along which t xompute de difference (default -1)

    Returns
    -------
    dthetas : ndarray, pbc corrected angle differences

    '''
    thetas = np.atleast_1d(thetas)
    if thetas.size == 1:
        return None
    if thetas.ndim == 1:
        return _1d_pbc_dtheta(thetas)

    dthetas = np.apply_along_axis(_1d_pbc_dtheta,
                                  axis, thetas, False)
    return dthetas


def _1d_pbc_dtheta(thetas):
    """Angular difference respecting periodic 2\pi
    boundary conditions"""
    dthetas = np.diff(thetas)
    dthetas[dthetas > np.pi] -= 2 * np.pi
    dthetas[dthetas < - np.pi] += 2 * np.pi
    return dthetas


def _1d_continuous_thetas(thetas, return_dtheta=True):
    """
    """
    theta0 = thetas[0]
    dthetas = _1d_pbc_dtheta(thetas)
    thetas_out = np.zeros(thetas.size)
    thetas_out[1:] = dthetas.cumsum()
    thetas_out = thetas_out + theta0
    if return_dtheta:
        return thetas_out, dthetas
    else:
        return thetas_out
