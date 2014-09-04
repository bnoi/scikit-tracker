# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from scipy.interpolate import splev, splrep

import logging
log = logging.getLogger(__name__)

__all__ = ["do_pca", "time_interpolate", "back_proj_interp",
           "back_proj_pca", "transformations_matrix", "interp_series"]


def do_pca(trajs,
           pca=None,
           coords=['x', 'y', 'z'],
           suffix='_pca',
           append=False, return_pca=False):
    '''
    Performs a principal component analysis on the input coordinates
    suffix is only applied when appending
    '''
    if pca is None:
        pca = PCA()
    if not np.all(np.isfinite(trajs[coords])):
        log.warning('''Droping non finite values before performing PCA''')

    rotated_ = pd.DataFrame(pca.fit_transform(trajs[coords].dropna()))
    rotated_.set_index(trajs[coords].dropna().index, inplace=True)
    rotated = pd.DataFrame(columns=coords,
                           index=trajs.index)
    rotated.loc[rotated_.index] = rotated_
    rotated['t'] = trajs.t

    if append:
        for pca_coord in [c + suffix for c in coords]:
            trajs[pca_coord] = rotated[pca_coord]
        if return_pca:
            return trajs, pca
        else:
            return trajs
    if return_pca:
        return rotated, pca
    else:
        return rotated


def _grouped_pca(trajs, pca, coords, group_kw):
    return trajs.groupby(**group_kw).apply(
        lambda df: pca.fit_transform(df[coords].dropna()),
        coords)


def time_interpolate(trajs, sampling=1,
                     s=0, k=3,
                     coords=['x', 'y', 'z']):
    """Interpolates each segment of the trajectories along time using `scipy.interpolate.splrep`

    Parameters
    ----------
    sampling : int,
        Must be higher or equal than 1, will add `sampling - 1` extra points
        between two consecutive original data point. Sub-sampling is not supported.

    coords : tuple of column names, default `('x', 'y', 'z')`
       the coordinates to interpolate.

     s : float
        A smoothing condition. The amount of smoothness is determined by satisfying the conditions:
        sum((w * (y - g))**2,axis=0) <= s where g(x) is the smoothed interpolation of (x,y). The
        user can use s to control the tradeoff between closeness and smoothness of fit. Larger s
        means more smoothing while smaller values of s indicate less smoothing. Recommended values
        of s depend on the weights, w. If the weights represent the inverse of the standard-
        deviation of y, then a good s value should be found in the range (m-sqrt(2*m),m+sqrt(2*m))
        where m is the number of datapoints in x, y, and w. default : s=m-sqrt(2*m) if weights are
        supplied. s = 0.0 (interpolating) if no weights are supplied.

    k : int
       The order of the spline fit. It is recommended to use cubic splines.
       Even order splines should be avoided especially with small s values.
       1 <= k <= 5

    Returns
    -------
    interpolated : a :class:`pandas.Dataframe` instance
       The interpolated values, with column names given by `coords` plus the computed speeds (first
       order derivative) and accelarations (second order derivative) if `k` > 2

    Notes
    -----
    - The returned DataFrame is NOT indexed like the input (in particular for `t_stamp`).
    - It is also NOT casted to a Trajectories instance.
    - The `s` and `k` arguments are passed to `scipy.interpolate.splrep`, see this function
      documentation for more details
    - If a segment is too short to be interpolated with the passed order `k`, the order will be
      automatically diminished.
    - Segments with only one point will be returned as is
    """
    interpolated = trajs.groupby(level='label').apply(_segment_interpolate_,
                                                      sampling=sampling, s=s, k=k,
                                                      coords=coords)
    interpolated = interpolated.swaplevel(
        't_stamp', 'label').sortlevel(['t_stamp', 'label'])
    return interpolated


def _segment_interpolate_(segment, sampling, s=0, k=3,
                          coords=['x', 'y', 'z']):
    """
    """

    corrected_k = k
    while segment.shape[0] <= corrected_k:
        corrected_k -= 2

    t_stamps_in = segment.index.get_level_values('t_stamp').values
    t_stamp0, t_stamp1 = t_stamps_in[0], t_stamps_in[-1]
    t0, t1 = segment.t.iloc[0], segment.t.iloc[-1]
    t_stamps = np.arange(t_stamp0*sampling,
                         t_stamp1*sampling+1, dtype=np.int)
    times = np.linspace(t0, t1, t_stamps.size)
    t_stamps = pd.Index(t_stamps, dtype=np.int, name='t_stamp')
    tmp_df = pd.DataFrame(index=t_stamps)
    tmp_df['t'] = times
    if segment.shape[0] < 2:
        for coord in coords:
            tmp_df[coord] = segment[coord].values
            tmp_df['v_'+coord] = np.nan
            tmp_df['a_'+coord] = np.nan
        return tmp_df
        #pass

    tck = _spline_rep(segment, coords, s=s, k=corrected_k)

    for coord in coords:
        tmp_df[coord] = splev(times, tck[coord], der=0)
        tmp_df['v_'+coord] = splev(times, tck[coord], der=1)
        if k > 2:
            if corrected_k > 2:
                tmp_df['a_'+coord] = splev(times, tck[coord], der=2)
            else:
                tmp_df['a_'+coord] = times * np.nan
    return tmp_df


def _spline_rep(df, coords=('x', 'y', 'z'), s=0, k=3):
    time = df.t
    tcks = {}
    for coord in coords:
        tcks[coord] = splrep(time, df[coord].values, s=s, k=k)
    return pd.DataFrame.from_dict(tcks)


def back_proj_interp(interpolated, orig, sampling):
    ''' back_proj_interp(interpolated, trajs, 3).iloc[0].x - trajs.iloc[0].x = 0
    '''
    back_t_stamps = orig.index.get_level_values('t_stamp')
    back_labels = orig.index.get_level_values('label')

    back_index = pd.MultiIndex.from_arrays([back_t_stamps,
                                            back_labels], names=['t_stamp', 'label'])
    interp_index = pd.MultiIndex.from_arrays([back_t_stamps*sampling,
                                              back_labels], names=['t_stamp', 'label'])
    back_projected_ = interpolated.loc[interp_index]
    back_index = pd.MultiIndex.from_arrays([back_t_stamps, back_labels],
                                           names=['t_stamp', 'label'])
    back_projected = back_projected_.set_index(back_index)
    return back_projected


def back_proj_pca(rotated, pca, coords):

    back_projected_ = pca.inverse_transform(rotated[coords])

    back_t_stamps = rotated.index.get_level_values('t_stamp')
    back_labels = rotated.index.get_level_values('label')
    back_index = pd.MultiIndex.from_arrays([back_t_stamps, back_labels],
                                           names=['t_stamp', 'label'])
    back_projected = pd.DataFrame(back_projected_, index=back_index, columns=coords)
    for col in set(rotated.columns) - set(back_projected.columns):
        back_projected[col] = rotated[col]
    return back_projected


def transformations_matrix(center, vec):
    """Build transformation matrix:
    - translation : from (0, 0) to a point (center)
    - rotation : following angle between (1, 0) and vec

    Parameters
    ----------
    center : list or np.ndarray
    vec : list or np.ndarray

    Returns
    -------
    The transformation matrix, np.ndarray.
    """

    # Setup vectors
    origin_vec = np.array([1, 0])
    current_vec = vec / np.linalg.norm(vec)

    # Find the rotation angle
    a = origin_vec
    b = current_vec
    theta = np.arctan2(a[1], a[0]) + np.arctan2(b[1], b[0])

    # Build rotation matrix
    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]], dtype="float")

    # Build translation matrix
    T = np.array([[1, 0, -center[0]],
                  [0, 1, -center[1]],
                  [0, 0, 1]], dtype="float")

    # Make transformations from R and T in one
    A = np.dot(T.T, R)

    return A


def interp_series(series, new_index):
    """Numpy API like pandas linear interpolation.

    Parameters
    ----------
    series : :class:`pandas.Series`
        Index should  x-coordinates of the data points and column y-coordinates of the data points.
    new_index : np.array
        The x-coordinates of the interpolated value.

    Return
    ------
    :class:`pandas.Series` of interpolated values.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from sktracker.trajectories.measures.transformation import interp_series
    >>> series = pd.Series([0, 10, 20, 40, 50, 60], index=[0, 1, 2, 4, 5, 6])
    >>> new_index = np.arange(0.5, 7.5, 1)
    >>> inter = interp_series(series, new_index)
    >>> print(inter)
    0.5     5
    1.5    15
    2.5    25
    3.5    35
    4.5    45
    5.5    55
    6.5    60
    dtype: float64
    """

    new_series = pd.Series(index=new_index)
    series_inter = pd.concat([series, new_series]).sort_index().interpolate(method='index')
    series_inter = series_inter.reindex(new_series.index)

    if series_inter.ndim == 2:
        series_inter = series_inter.drop(0, axis=1)

    return series_inter
