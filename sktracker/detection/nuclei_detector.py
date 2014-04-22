
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import logging
import itertools

import numpy as np
import pandas as pd

from scipy.spatial.distance import squareform, pdist
from scipy.cluster import hierarchy
from scipy import ndimage

from skimage.filter import rank, threshold_otsu
from skimage.morphology import disk, watershed
from skimage.feature import peak_local_max
from skimage.measure import regionprops

from ..io import ObjectsIO
from ..trajectories import Trajectories

log = logging.getLogger(__name__)

__all__ = []

DEFAULT_PARAMETERS = {'segment_method': 'otsu',
                      'correction': 1.,
                      'smooth': 10,
                      'min_radius': 2.,
                      'max_radius': 8.,
                      'num_cells': 8,
                      'min_z_size': 4.
                      }


def nuclei_detector(data_iterator,
                    metadata={},
                    parameters={},
                    parallel=False,
                    verbose=False,
                    mapper=None,
                    show_progress=False):
    '''
    TODO

    Parameters
    ----------
    data_iterator : Python iterator over dataset
    metadata: dict
    parameters : dict
    parallel : bool
    verbose : bool
    mapper : bool
    show_progress : bool

    Returns
    -------
    trajs : :class:`pd.DataFrame`
    '''

    _parameters = DEFAULT_PARAMETERS.copy()
    _parameters.update(parameters)
    parameters = _parameters

    parameters['min_z_size'] = parameters['min_z_size'] / metadata['PhysicalSizeZ']
    parameters['min_radius'] /= metadata['PhysicalSizeX']
    parameters['max_radius'] /= metadata['PhysicalSizeX']

    arguments = zip(data_iterator, itertools.repeat(parameters))
    if parallel and mapper is not None:
        results = mapper.map(detect_one_stack,
                             arguments)
    else:
        results = map(detect_one_stack,
                      arguments)

    raw_cell_positions = {}
    for i, result in enumerate(results):
        if 'positions' in result:
            raw_cell_positions[i] = result['positions']
    if not len(raw_cell_positions):
        log.warning('No cell detected anywhere')
        return pd.DataFrame([])
    nuclei_positions = pd.concat(
        raw_cell_positions,
        keys=raw_cell_positions.keys(),
        names=('t_stamp', 'label'))

    real_times = nuclei_positions.index.get_level_values('t_stamp').astype(np.float)
    real_times *= metadata['TimeIncrement']
    nuclei_positions['t'] = real_times
    nuclei_positions['x'] *=  metadata['PhysicalSizeX']
    nuclei_positions['y'] *=  metadata['PhysicalSizeY']
    nuclei_positions['z'] *=  metadata['PhysicalSizeZ']
    nuclei_positions['w'] *=  metadata['PhysicalSizeX']
    return Trajectories(nuclei_positions)


def detect_one_stack(args, full_output=False):

    z_stack, parameters = args
    if len(z_stack.shape) == 2:
        z_stack = z_stack[np.newaxis, ...]
    labeled_stack = label_stack(z_stack, parameters)
    if labeled_stack is None:
        return {}
    all_props = get_regionprops(labeled_stack,
                                z_stack, parameters)
    if not len(all_props):
        log.warning('No cell found after labelling')
        if full_output:
            output = {'labeled_stack': labeled_stack}
            return output
        else:
            return {}
    if z_stack.shape[0] == 1:
        positions = all_props.copy()
        positions.index = pd.Index(range(all_props.shape[0]))
        if full_output:
            output = {'positions': positions,
                      'labeled_stack': labeled_stack}
        else:
            output = {'positions': positions}
        return output

    agregated_props = cluster_regions(all_props, parameters)
    positions = get_cell_positions(agregated_props, parameters)

    if not len(positions):
        output = {'all_props': all_props,
                  'agregated_props': agregated_props,
                  'labeled_stack': labeled_stack}
        return output
    if full_output:
        output = {'positions': positions,
                  'all_props': all_props,
                  'agregated_props': agregated_props,
                  'labeled_stack': labeled_stack}
    else:
        output = {'positions': positions,}
    return output


def label_stack(z_stack, parameters):
    '''
    Apply an automated threshold and a watershed algorithm to
    label cells in each planes of the stack

    Parameters:
    -----------
    z_stack: 3d array of shape (nz, nx, ny)

    Returns:
    --------
    labeled_stack: 3d array of the same shape as z_stack,
    with each detected region labeled
    '''
    segment_method = parameters['segment_method']
    correction = parameters['correction']
    labeled_stack = np.zeros(z_stack.shape, dtype=np.uint8)
    max_int_proj = z_stack.max(axis=0)
    thresh = None

    if segment_method == 'otsu':
        thresh = threshold_otsu(max_int_proj) * correction
    elif segment_method == 'naive':
        thresh = max_int_proj.max() * correction
    else:
        err_string = ('Segmentation method {}'
                      'is not implemented'.format(segment_method))
        raise NotImplementedError(err_string)
    while thresh > z_stack.max():
        log.warning('''Reducing threshold''')
        thresh *= 0.9
    for n, frame in enumerate(z_stack):
        labeled_stack[n] = label_from_thresh(frame, thresh, parameters)
    return labeled_stack


def label_from_thresh(frame, thresh, parameters):

    smooth = parameters['smooth']
    min_radius = parameters['min_radius']
    image = rank.median(frame.copy(), disk(smooth))
    image = rank.enhance_contrast(image, disk(smooth))
    im_max = image.max()
    if im_max < thresh:
        return np.zeros(image.shape, dtype=np.int32)
    else:
        image = frame > thresh
        distance = ndimage.distance_transform_edt(image)
        local_maxi = peak_local_max(distance,
                                    min_distance=np.int(min_radius),
                                    indices=False, labels=image)
        markers = ndimage.label(local_maxi)[0]
        return watershed(-distance, markers, mask=image)


def get_regionprops(labeled_stack, z_stack, parameters):
    '''
    Computes the area, centroid position and mean intensity
    of all the regions
    Removes the regions with typical size outside [min_radius, max_radius]

    returns a DataFrame with colmuns ('x', 'y', 'z', 'I', 'w')
    '''

    min_radius = parameters['min_radius']
    max_radius = parameters['max_radius']
    all_props = []
    #properties = ['Area', 'WeightedCentroid', 'MeanIntensity']
    columns = ('x', 'y', 'z', 'I', 'w')
    indices = []
    for z, frame in enumerate(labeled_stack):
        f_prop = regionprops(frame.astype(np.int),# properties,
                             intensity_image=z_stack[z])
        for d in f_prop:
            radius = (d.area / np.pi)**0.5
            if (min_radius  < radius < max_radius):
                all_props.append([d.centroid[0],
                                  d.centroid[1],
                                  z, d.mean_intensity * d.area,
                                  radius])
                indices.append((d.label, z))
    if not len(indices):
        return pd.DataFrame([], index=[])
    indices = pd.MultiIndex.from_tuples(indices, names=('label', 'z'))
    all_props = pd.DataFrame(all_props, index=indices, columns=columns)
    return all_props


def cluster_regions(all_props, parameters):

    radius = parameters['max_radius']
    num_cells = parameters['num_cells']
    n_clusters = min(num_cells, all_props.shape[0])
    if not n_clusters:
        return None
    if n_clusters == 1:
        log.warning('Only one cluster')
        return all_props
    positions = all_props[['x', 'y']].copy()

    if all_props.shape[0] < 3:
        return all_props[['x', 'y', 'z', 'w', 'I']]

    # Hierarchical clustering
    dist_mat = squareform(pdist(positions.values))
    link_mat = hierarchy.linkage(dist_mat)
    cluster_idx = hierarchy.fcluster(link_mat, radius,
                                     criterion='distance')
    all_props['label'] = cluster_idx
    all_props.set_index('label', drop=False, append=False, inplace=True)
    all_props.index.name = 'label'
    all_props = all_props.sort_index()

    lbl_bincount = np.bincount(
        all_props.index.astype(np.uint16))[all_props.index.unique()]
    min_z_size = parameters['min_z_size']
    shorts = all_props.index.unique()[lbl_bincount < min_z_size]
    all_props = all_props.drop(shorts)
    all_props.set_index('label', drop=True, append=False, inplace=True)
    all_props.index.name = 'label'
    all_props = all_props.sort_index()
    return all_props


def get_cell_positions(all_props, interpolate=True):

    # Intensity should be summed, not averaged
    intensities = all_props['I'].groupby(
        level='label').sum()
    intensities /= intensities.max()
    cell_positions = all_props.groupby(
        level='label').apply(df_average, 'I')
    cell_positions['I'] = intensities
    return cell_positions


def df_average(df, weights_column):
    values = df.copy().iloc[0]
    norm = df[weights_column].sum()
    for col in df.columns:
        try:
            v = (df[col] * df[weights_column]).sum() / norm
        except TypeError:
            v = df[col].iloc[0]
        values[col] = v
    return values
