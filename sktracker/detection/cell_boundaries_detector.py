
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import logging
log = logging.getLogger(__name__)

import pandas as pd
import numpy as np

from scipy import integrate
from skimage.filter import threshold_otsu
from skimage.measure import regionprops
from skimage.segmentation import clear_border
from skimage.morphology import binary_closing
from skimage.morphology import square
from skimage.morphology import medial_axis
from skimage.morphology import label

from ..utils.progress import print_progress

__all__ = []

DEFAULT_PARAMETERS = {'object_height': 3,
                      'minimal_area': 160}


def cell_boundaries_detector(data_iterator,
                             metadata,
                             show_progress=False,
                             parameters={}):
    """
    Find cell boundary in bright field microscopy image.

    Parameters
    ----------
    data_iterator : python iterator
        To iterate over data.
    metadata : dict
        Metadata to scale detected peaks and parameters.
    show_progress : bool (default: False)
        Print progress bar during detection.
    verbose : bool (default: True)
        Display informations during detection.
    parameters : dict
        object_height : float
            Typical size of the object in um.
        minimal_area : float
            Typical area of the object in um^2.

    Returns
    ------()
    shapes : :class:`pd.DataFrame`
        Contains cell boundary properties for each time_stamp
    """

    _parameters = DEFAULT_PARAMETERS.copy()
    _parameters.update(parameters)
    parameters = _parameters

    # Load parameters
    sigma = parameters['object_height'] / metadata['PhysicalSizeZ']
    minimal_area = parameters['minimal_area'] / metadata['PhysicalSizeX']

    sizeX = metadata['SizeX']
    sizeY = metadata['SizeY']

    # calculate the correlation image from the z-stack
    cellprop = []
    t_tot = metadata['SizeT']
    for t, imt in enumerate(data_iterator):

        if show_progress:
            p = int(float(t + 1) / t_tot * 100.)
            print_progress(p)

        if np.any(imt) != 0:
            corr = np.zeros((sizeY, sizeX))

            for y, x in np.ndindex(sizeY, sizeX):
                Iz = imt[:, y, x]
                z = np.array(range(len(Iz)))
                zf = len(Iz) / 2
                corr[y, x] = integrate.simps(Iz[z] * (z - zf) * np.exp(-(zf - z) ** 2 /
                                             (2 * sigma ** 2)), z)

            # create binary mask of the correlation image
            thresh = threshold_otsu(corr)
            mask = corr > thresh

            area = 0
            n = 2

            prevarea = None
            prevcellprop = None

            # un seuil pas trop petit au cas où il resterait des petits objets
            # dans l'image
            while area < minimal_area and prevarea != area:
                tophat = binary_closing(mask, square(n))
                n += 1
                skel = medial_axis(tophat)
                skel = (skel - 1) * (-1)
                cleared = clear_border(skel)
                labelized = label(cleared, 8, 0) + 1

                # add cell characteristic in the cellprop list
                if np.any(labelized):
                    prevcellprop = regionprops(
                        labelized, intensity_image=corr)[0]

                prevarea = area
                if prevcellprop:
                    area = prevcellprop['area']

            if prevcellprop:
                cellprop.append(prevcellprop)

            else:
                if len(cellprop) >= 1:
                    cellprop.append(cellprop[-1])
                else:
                    cellprop.append(None)
        else:
                if len(cellprop) >= 1:
                    cellprop.append(cellprop[-1])
                else:
                    cellprop.append(None)

    print_progress(-1)

    # class cell morphology in time in the props Dataframe (time, centroid X,
    # centroid Y, ...)
    listprop = ['centroid_x', 'centroid_y', 'orientation', 'major_axis', 'minor_axis']
    cell_Prop = np.zeros((len(listprop) + 1, metadata["SizeT"]))

    for i in range(metadata["SizeT"]):
        if cellprop[i]:
            cell_Prop[0, i] = i
            cell_Prop[1, i] = cellprop[i]['centroid'][0] * metadata['PhysicalSizeX']
            cell_Prop[2, i] = cellprop[i]['centroid'][1] * metadata['PhysicalSizeX']
            cell_Prop[3, i] = cellprop[i]['orientation']
            cell_Prop[4, i] = cellprop[i]['major_axis_length'] * metadata['PhysicalSizeX']
            cell_Prop[5, i] = cellprop[i]['minor_axis_length'] * metadata['PhysicalSizeX']

    cell_Prop = cell_Prop.T
    props = pd.DataFrame(cell_Prop, columns=['t_stamp'] + listprop)
    props = props.set_index('t_stamp')
    props['t'] = props.index.get_level_values('t_stamp') * metadata['TimeIncrement']
    props = props.astype(np.float)

    if np.all(props == 0):
        return pd.DataFrame([])
    else:
        return props
