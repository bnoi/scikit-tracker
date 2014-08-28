# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pandas as pd

from .measure_decorators import trajs_measure
from .measure_decorators import p2p_measure

import logging
log = logging.getLogger(__name__)


# This should be a Trajectories attribute
def by_segments(trajs, group_keys=False, **kwargs):
    return trajs.groupby(level='label',
                         group_keys=group_keys, **kwargs)

# Point to point methods


@p2p_measure
def p2p_cum_dir(trajs, t_stamp0, t_stamp1,
                coords=['x', 'y', 'z'],
                append=False):
    '''Computes the ratio between the net displacement and the
    cumulated displacement between t_stamp0 and t_stamp1 over coords

    call signature:
      p2p_cum_dir(trajs, t_stamp0, t_stamp1,
                  coords=['x', 'y', 'z'],
                  append=False)
    '''
    if not 'cum_disp' in trajs.columns:
        trajs['cum_disp'] = cum_disp(trajs)['cum_disp']
    shifted = by_segments(trajs).apply(p2p_dif_, t_stamp0, t_stamp1,
                                       [coords[0], 'cum_disp'])
    measure = shifted[coords[0]] / shifted['cum_disp']
    return measure


@p2p_measure
def p2p_directionality(trajs, t_stamp0, t_stamp1,
                       coords=['x', 'y', 'z']):
    '''Computes the ratio between the displacement along the first coordinate
    and the net displacement between t_stamp0 and t_stamp1
    '''
    shifted = by_segments(trajs).apply(p2p_dif_, t_stamp0, t_stamp1,
                                       coords)
    measure = shifted[coords[0]] / np.linalg.norm(shifted[coords],
                                                  axis=1)
    return measure


@p2p_measure
def p2p_processivity(trajs, t_stamp0, t_stamp1,
                     signed=True,
                     coords=['x', 'y', 'z']):
    '''Computes
    '''
    if not 'cum_disp' in trajs.columns:
        trajs['cum_disp'] = cum_disp(trajs, coords)['cum_disp']

    shifted = by_segments(trajs).apply(p2p_dif_, t_stamp0, t_stamp1,
                                       coords+['cum_disp'])

    if signed:
        measure = (np.linalg.norm(shifted[coords], axis=1) /
                   shifted['cum_disp']) * np.sign(shifted[coords[0]])
    else:
        measure = (np.linalg.norm(shifted[coords], axis=1) /
                   shifted['cum_disp'])
    return measure


@trajs_measure
def cum_disp(trajs, coords=['x', 'y', 'z']):
    '''
    '''
    measure = by_segments(trajs).apply(cumulative_displacement_,
                                       coords=coords)
    return measure


### Sliding methods
@trajs_measure
def sld_dir(trajs, window,
            coords=['x', 'y', 'z']):
    '''
    '''
    shifted = by_segments(trajs).apply(shifted_dif_, window, coords)
    measure = (shifted[coords[0]] / np.linalg.norm(shifted[coords],
                                                   axis=1))
    return measure


@trajs_measure
def sld_processivity(trajs, window, signed=True,
                     coords=['x', 'y', 'z']):
    '''
    '''
    if not 'cum_disp' in trajs.columns:
        trajs['cum_disp'] = cum_disp(trajs, coords)['cum_disp']

    shifted = by_segments(trajs).apply(shifted_dif_, window,
                                       coords+['cum_disp'])
    if signed:
        measure = np.sign(shifted[coords[0]]) * (np.linalg.norm(shifted[coords], axis=1) /
                                                 shifted['cum_disp'])
    else:
        measure = np.linalg.norm(shifted[coords], axis=1) / shifted['cum_disp']
    return measure


@trajs_measure
def sld_cum_dir(trajs, window, coords=['x', 'y', 'z']):
    '''
    Window is expressed in t_stamps
    '''
    if not 'cum_disp' in trajs.columns:
        trajs['cum_disp'] = cum_disp(trajs, coords)['cum_disp']

    shifted = by_segments(trajs).apply(shifted_dif_, window,
                                       [coords[0], 'cum_disp'])
    measure = shifted[coords[0]] / shifted['cum_disp']
    return measure


def get_MSD(trajs):
    '''
    Compute the mean square displacement for each segment.
    '''
    dts = trajs.t_stamps - trajs.t_stamps[0]
    MSD = by_segments(trajs, group_keys=True).apply(compute_MSD_, dts)
    MSD = MSD.sortlevel(['Dt_stamp', 'label']).swaplevel('Dt_stamp', 'label')
    MSD['Dt'] = trajs.t.values - trajs.t.iloc[0]
    return MSD

## Segment pseudo methods


#@segment_measure
def shifted_dif_(segment, shift, coords):
    '''
    '''
    left_shift = - np.floor(shift/2).astype(np.int)
    right_shift = np.ceil(shift/2).astype(np.int)
    return segment[coords].shift(left_shift) - segment[coords].shift(right_shift)


#@segment_measure
def p2p_dif_(segment, t_stamp0, t_stamp1, coords):
    '''
    Computes the difference of coordinates coords between t_stamp1 and t_stamp0
    '''
    t_stamps = segment.index.get_level_values('t_stamp')
    if not {t_stamp0, t_stamp1}.issubset(set(t_stamps)):
        diff = segment.loc[t_stamps[0]][coords]*np.nan
    else:
        diff = segment[coords].loc[t_stamp1] - segment[coords].loc[t_stamp0]
    return diff


#@segment_measure
def cumulative_displacement_(segment, coords):
    '''Computes the cumulated displacement of the segment given by

    .. math::

        \begin{aligned}
        D(0) &= 0\\
        D(t) &= \sum_{i=1}^{t} \left((x_i - x_{i-1})^2 + (y_i - y_{i-1})^2 + (z_i -
        z_{i-1})^2\right)^{1/2}\\
        \end{aligned}
    '''
    x, y, z = coords
    displacement = np.sqrt(segment[x].diff()**2
                           + segment[y].diff()**2
                           + segment[z].diff()**2)
    displacement = displacement.cumsum()
    displacement.iloc[0] = 0
    #segment['fwd_frac'] = (segment[x] - segment[x].iloc[0]) / segment['disp']
    return displacement


#@segment_measure
def compute_MSD_(segment, dts, coords=['x', 'y', 'z']):
    '''Computes the mean square displacement of the segment given by

    .. math::

        \begin{aligned}
        \mbox{MSD}(\Delta t) &=  \frac{\sum_0^{T - \Delta t}
            \left(\mathbf{r}(t + \Delta t)  - \mathbf{r}(t) \right)^2}{(T - \Delta t) / \delta t}
        \end{aligned}
    '''
    dts = np.asarray(dts, dtype=np.int)
    msds = pd.DataFrame(index=pd.Index(dts, name='Dt_stamp'),
                        columns=['MSD', 'MSD_std'], dtype=np.float)
    msds.loc[0] = 0, 0
    for dt in dts[1:]:
        msd = ((segment[coords]
                - segment[coords].shift(dt)).dropna()**2).sum(axis=1)
        msds.loc[dt, 'MSD'] = msd.mean()
        msds.loc[dt, 'MSD_std'] = msd.std()
    return msds
