# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pandas as pd
from ..trajectories import Trajectories

import logging
log = logging.getLogger(__name__)


###trajectories pseudo methods
def radial_speed(trajs, in_coords=['rho', 'theta'],
                 from_polar=True,
                 smooth=0,
                 append=False,
                 out_coords=['v_rad', 'v_orad'] ):
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
    radial_speed_c, ortho_rad_speed_c = out_coords
    radial_speed = intp_polar['v_rho']
    ortho_rad_speed = intp_polar['rho'] * intp_polar['v_theta']
    speeds = pd.DataFrame.from_dict({radial_speed_c: radial_speed,
                                     ortho_rad_speed_c: ortho_rad_speed})
    speeds.set_index(intp_polar.index)
    speeds = speeds.loc[trajs.index]
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

    Parameters :
    ------------
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
    polar_trajs = pd.DataFrame.from_dict({theta_coord:thetas,
                                         rho_coord:rhos})
    polar_trajs.set_index(trajs.index)
    if not periodic:
        polar_trajs = polar_trajs.groupby(level='label').apply(continous_theta_,
                                                               theta_coord, get_dtheta)
    elif get_dtheta:
        polar_trajs['d'+theta_coord] = polar_trajs.groupby(level='label').apply(periodic_dtheta_,
                                                                                theta_coord)
    if append:
        for coord in polar_trajs.columns:
            trajs[coord] = polar_trajs[coord]
            return trajs
    return polar_trajs


### segment method
def continous_theta_(segment, coord='theta', get_dtheta=True):

    out = _continuous_theta(segment[coord].values,
                            return_dtheta=get_dtheta)
    if get_dtheta:
        thetas, dthetas = out
        segment['d'+coord] = 0
        segment['d'+coord].iloc[1:] = dthetas
        segment[coord] = thetas
    else:
        thetas = out
        segment[coord] = thetas
    return segment

def periodic_dtheta_(segment, coord='theta'):
    return _periodic_dtheta(segment[coord].values)


### array methods
def _continuous_theta(thetas, return_dtheta=True, axis=-1):
    '''Shifts the passed angles by multiples of ::math:2\np.pi such that
    the result is continuous (i.e. accumulating circles).

    If `return_dtheta` is True, also returns the difference between
    two consecutive values, corrected for periodic boundary conditions
    between ::math:\pi: and ::math:-\pi:

    Parameters :
    ------------
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

    Parameters :
    ------------
    thetas : ndarray, angle vaues in radians
    axis : int, default -1
        the axis along which t xompute de difference (default -1)

    Returns :
    ---------
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
