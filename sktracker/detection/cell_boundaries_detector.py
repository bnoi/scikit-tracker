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

__all__ = ['peak_detector']

DEFAULT_PARAMETERS = {'sigma': 3,
                      'minimal_area': 5,
                      }

def cell_boundaries_detector(data_iterator,
                             metadata,
                             verbose=True,
                             show_progress=False,
                             parameters={}):
    """
    Find cell boundary in BF microscopy image.

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
            - sigma: float
                Width (in um) of the sliding window over which the hypothesis ratio
                is computed :math:`w_s` in the article. It should be wide enough
                to contain some background to allow a proper noise evaluation.
            - minimal_area: int
                Minimal area to find (in um)

    Return
    ------
    `pd.DataFrame` : contains cell boundary properties for each T
    """

    if not verbose:
        log.disabled = True

    _parameters = DEFAULT_PARAMETERS.copy()
    _parameters.update(parameters)
    parameters = _parameters

    # Scale parameters in pixels
    parameters['minimal_area'] /= metadata['PhysicalSizeX']

    # Find number of stacks to process
    # Only iteration over T and Z are assumed
    n_stack = metadata['SizeT'] * metadata['SizeZ']

    for t, imt in enumerate(data_iterator()):

        if show_progress:
            p = int(float(t + 1) / t_tot * 100.)
            print_progress(p)

        if (np.any(imt) != 0 or (t != 0 and not np.array_equal(imt, im[t - 1]))):
            corr = np.zeros((im.shape[-2], im.shape[-1]))
            for x, y in np.ndindex(imt.shape[-2], imt.shape[-1]):
                Iz = imt[:, x, y]
                z = np.array(range(len(Iz)))
                zf = len(Iz) / 2
                corr[x, y] = integrate.simps(
                    Iz[z] * (z - zf) * np.exp(-(zf - z) ** 2 / (2 * sigma ** 2)), z)

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
    listprop = ['centroid_x', 'centroid_y',
                'orientation', 'major_axis', 'minor_axis']
    cell_Prop = np.zeros((len(listprop) + 1, metadata["SizeT"]))

    for i in range(metadata["SizeT"]):
        if cellprop[i]:
            cell_Prop[0, i] = i
            cell_Prop[1, i] = cellprop[i]['centroid'][0]
            cell_Prop[2, i] = cellprop[i]['centroid'][1]
            cell_Prop[3, i] = cellprop[i]['orientation']
            cell_Prop[4, i] = cellprop[i]['major_axis_length']
            cell_Prop[5, i] = cellprop[i]['minor_axis_length']

    cell_Prop = cell_Prop.T
    props = pd.DataFrame(cell_Prop, columns=['t'] + listprop)
    props = props.set_index('t')

    if np.all(props == 0):
        return pd.DataFrame([])
    else:
        return props
