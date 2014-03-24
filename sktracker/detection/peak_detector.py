import os
import logging
import subprocess
import multiprocessing
import itertools

from scipy.optimize import leastsq
from skimage import feature

import numpy as np

from ..utils import print_progress

log = logging.getLogger(__name__)

__all__ = ['peak_detector']

DEFAULT_PARAMETERS = {'w_s': 0.7,
                      'peak_radius': 0.2,
                      'threshold': 27.,
                      'max_peaks': 1e4
                      }

def peak_detector(data_iterator,
                  metadata,
                  parallel=True,
                  verbose=True,
                  show_progress=False,
                  parameters={}):
    """Gaussian peak detection described in Segré et al. Nature Methods, (2008).

    Parameters
    ----------
    data_iterator : python iterator
        To iterate over data.
    metadata : dict
        Metadata to scale detected peaks and parameters.
    parallel : bool
        Used several processes at once.
    show_progress : bool (default: False)
        Print progress bar during detection.
    verbose : bool (default: True)
        Display informations during detection.
    parameters : dict
        Contains gaussian detection algorithm parameters:
            - w_s: int, optional
                Width (in um) of the sliding window over which the hypothesis ratio
                is computed :math:`w_s` in the article. It should be wide enough
                to contain some background to allow a proper noise evaluation.
            - peak_radius: float, optional
                Typical radius (in um) of the peaks to detect. It must be higher than one
                (as peaks less that a pixel wide would yield bogus results
            - threshold: float, optional
                Criterium for a positive detection (i.e. the null hypothesis is false).
                Corresponds to the :mat:`\chi^2` parameter in the Constant False
                Alarm Rate section of the article supplementary text (p. 12).
                A higher `threshold` corresponds to a more stringent test.
                According to the authors, this parameters needs to be adjusted
                once for a given data set.
            - max_peaks : int, optional
                Deflation loop will stop if detected peaks is higher than max_peaks.

    Returns
    -------
    `pandas.DataFrame` array containing detected peaks.
    """

    if not verbose:
        log.disabled = True

    _parameters = DEFAULT_PARAMETERS
    _parameters.update(parameters)
    parameters = _parameters

    # Scale parameters in pixels
    parameters['w_s'] /= metadata['PhysicalSizeX']
    parameters['w_s'] = np.round(parameters['w_s'])
    parameters['peak_radius'] /= metadata['PhysicalSizeX']

    # Find number of stacks to process
    # Only iteration over T and Z are assumed
    t_position = metadata['DimensionOrder'].index('T')
    z_position = metadata['DimensionOrder'].index('Z')
    n_stack = metadata['Shape'][t_position] * metadata['Shape'][z_position]

    if parallel:

        # Snippet to allow multiprocessing while importing
        # module such as numpy (only needed on linux)
        if os.name == 'posix':
            subprocess.call("taskset -p 0xff %d" % os.getpid(),
                            shell=True, stdout=subprocess.DEVNULL)

        def init_worker():
            import signal
            signal.signal(signal.SIGINT, signal.SIG_IGN)

        ncore = multiprocessing.cpu_count() + 1
        log.info('Parallel mode enabled: %i cores will be used to process %i stacks' %
                 (ncore, n_stack))
        pool = multiprocessing.Pool(processes=ncore, initializer=init_worker)

    # Build arguments list
    arguments = zip(data_iterator,
                    itertools.repeat(parameters),
                    range(n_stack))

    try:
        # Launch peak_detection
        if parallel:
            results = pool.imap_unordered(find_gaussian_peaks, arguments)
        else:
            results = map(find_gaussian_peaks, arguments)

        all_peaks = []

        # Get unordered results and log progress
        for i, (pos, peaks) in enumerate(results):

            n_peaks = len(peaks)
            percent_progression = (i + 1) / n_stack * 100

            if show_progress:
                message = ("%i/%i - %i peaks detected on stack n°%i" %
                           ((i + 1), n_stack, n_peaks, pos))
                pprogress(percent_progression, message)

            elif verbose:
                log.info('Detection done for stack number %i: %i peaks detected (%i/%i - %i%%)' %
                     (pos, n_peaks, i + 1, n_stack, percent_progression))

            all_peaks.append((pos, peaks))

        if show_progress:
            pprogress(-1)

    except KeyboardInterrupt:
        if parallel:
            pool.terminate()
            pool.join()
        raise Exception('Detection has been canceled by user')

    if parallel:
        pool.close()
        pool.terminate()

    # Sort peaks and remove index used to sort
    all_peaks.sort(key=lambda x: x[0])
    all_peaks = [x[1] for x in all_peaks]

    # # Pre-processing peaks
    # index = []
    # peaks = []

    # for t, peak in enumerate(all_peaks):
    #     if peak.any():
    #         for i, p in enumerate(peak):
    #             index.append((t, i))
    #             peaks.append(p)

    # if not peaks:
    #     return pd.DataFrame([])

    return all_peaks
    # peaks = pd.DataFrame(peaks, columns=['x', 'y', 'w', 'I'], dtype='float')
    # peaks.index = pd.MultiIndex.from_tuples(index, names=['t_stamp', 'label'])

    # return peaks


def find_gaussian_peaks(args):
    """
    Buffer function for _find_gaussian_peaks
    """
    frame, detection_parameters, i = args
    return (i, _find_gaussian_peaks(frame, **detection_parameters))


def _find_gaussian_peaks(image, w_s=15, peak_radius=1.5,
                         threshold=27., max_peaks=1e4):
    """
    This function implements the Gaussian peak detection described
    in Segré et al. Nature Methods **5**, 8 (2008). It is based on a
    likelyhood ratio test on the presence or absence of a Gaussian
    peak on a patch moving over the input 2D image and a successive
    sub-pixel localization of the peaks by a least square fit.  This
    detection is followed recursively by a _deflation_ of the image
    from the detected peaks and a new detection, until no more peaks
    are found

    Parameters
    ----------

    image: a 2D array
        the input image
    w_s: int, optional
        the width of the sliding window over which the hypothesis ratio
        is computed :math:`w_s` in the article. It should be wide enough
        to contain some background to allow a proper noise evaluation.
    peak_radius: float, optional
        typical radius of the peaks to detect. It must be higher than one
        (as peaks less that a pixel wide would yield bogus results
    thershold: float, optional
        Criterium for a positive detection (i.e. the null hypothesis is false).
        Corresponds to the :mat:`\chi^2` parameter in the Constant False
        Alarm Rate section of the article supplementary text (p. 12).
        A higher `threshold` corresponds to a more stringent test.
        According to the authors, this parameters needs to be adjusted
        once for a given data set.

    Returns
    -------

    peaks: ndarray
        peaks is a Nx4 array, where N is the number of detected peaks in the
        image. Each line gives the x position, y position, width,
        and (background corrected) intensity of a detected peak (in that order).

    """
    peaks_coords = glrt_detection(image, peak_radius,
                                  w_s, threshold)
    peaks = gauss_estimation(image, peaks_coords, w_s)
    d_image = image_deflation(image, peaks, w_s)
    peaks_coords = glrt_detection(d_image, peak_radius,
                                  w_s, threshold)
    while len(peaks_coords) > 0 and len(peaks) < max_peaks:
        new_peaks = gauss_estimation(d_image, peaks_coords, w_s)
        # in case the 2D gauss fit fails
        if len(new_peaks) < 1:
            break
        peaks.extend(new_peaks[:])
        d_image = image_deflation(d_image, new_peaks, w_s)
        peaks_coords = glrt_detection(d_image, peak_radius,
                                      w_s, threshold)
    peaks = np.array(peaks)
    return peaks


def image_deflation(image, peaks, w_s):
    """
    Substracts the detected Gaussian peaks from the input image and
    returns the deflated image.
    """
    d_image = image.copy()
    for peak in peaks:
        xc, yc, width, I = peak
        xc_rel = w_s // 2 + xc - np.floor(xc)
        yc_rel = w_s // 2 + yc - np.floor(yc)
        low_x = int(xc - w_s // 2)
        low_y = int(yc - w_s // 2)

        params = xc_rel, yc_rel, width, I, 0
        deflated_peak = gauss_continuous(params, w_s)
        d_image[low_x:low_x + w_s,
                low_y:low_y + w_s] -= deflated_peak.reshape((w_s, w_s))
    return d_image


def gauss_estimation(image, peaks_coords, w_s):
    """
    Least square fit of a 2D Gauss peaks (with radial symmetry)
    on regions of width `w_s` centered on each element
    of `peaks_coords`.

    Parameters:
    ----------
    image : 2D array
        a greyscale 2D input image.
    peaks_coords: iterable of pairs of int.
       The peaks_coords should contain `(x, y)` pairs
       corresponding to the approximate peak center,
       in pixels.
    """
    peaks = []
    for coords in peaks_coords:
        low_x, low_y = coords - w_s // 2
        try:
            patch = image[low_x: low_x + w_s,
                          low_y: low_y + w_s]
            params, success = gauss_estimate(patch, w_s)
            xc, yc, width, I, bg = params
            if success and I > 0 and width < w_s:
                peaks.append([xc + low_x, yc + low_y, width, I])
        except IndexError:
            log.error('peak too close from the edge\n'
                      'use a smaller window\n'
                      'peak @ (%i, %i) discarded' % (coords[0], coords[1]))
            continue
    return peaks


def glrt_detection(image, r0, w_s, threshold):
    """
    Implements the Generalized Likelyhood Ratio Test, by
    computing equation 4 in Segré et al. Supplementary Note (p. 12)
    in a window sliding other the image.

    Parameters:
    ----------
    image: array
        the 2D input image
    r0: float
        the detected Gaussian peak 1/e radius
    w_s: int
        Size of the sliding window over which the test is
        computed ( :math:`w_s` in the article).
    threshold: float
        Criterium for a positive detection (i.e. the null hypothesis is false).
        Corresponds to the :mat:`\chi^2` parameter in the Constant False
        Alarm Rate section of the article supplementary text (p. 12).
        A higher `threshold` corresponds to a more stringent test.
        According to the authors, this parameters needs to be adjusted
        once for a given data set.

    Returns:
    --------

    peaks_coords: array
        An Nx2 array containing (x, y) pairs of the detected peaks
        in integer pixel coordinates.
    """

    if isinstance(image, np.ma.core.MaskedArray):
        mask = image.mask
        image = image.data
    elif isinstance(image, np.ndarray):
        mask = None
    else:
        raise Exception("Image has to be np.ndarray or np.ma.core.MaskedArray")

    w, h = image.shape
    g_patch = gauss_patch(r0, w_s)
    g_patch -= g_patch.mean()
    g_squaresum = np.sum(g_patch ** 2)

    hmap = []
    for i, j in np.ndindex((w - w_s, h - w_s)):
        h = hypothesis_map(image[i: i + w_s, j: j + w_s],
                           g_patch,
                           g_squaresum)
        hmap.append(h)
    hmap = np.array(hmap)

    try:
        hmap = -2 * hmap.reshape((w - w_s, h - w_s))
        peaks_coords = feature.peak_local_max(hmap, 3,
                                              threshold_abs=threshold)
        peaks_coords += w_s / 2
        if isinstance(mask, np.ndarray):
            peaks_coords = list(filter(lambda x: not mask[x[0], x[1]], peaks_coords))

        return peaks_coords

    except ValueError:
        return np.array([])


def hypothesis_map(patch, g_patch, g_squaresum):
    """
    Computes the ratio for a given patch position.
    """
    w_s = patch.shape[0]
    # mean = patch.mean()
    multiplicative = g_patch * patch

    intensity = multiplicative.sum()
    normalisation = w_s * patch.std()
    ratio = (w_s ** 2 / 2.) * np.log(1 - (intensity
                                          / normalisation) ** 2
                                     / g_squaresum)
    return ratio


def gauss_estimate(patch, w_s):
    """
    Least square 2D gauss fit
    """
    params0 = [w_s / 2., w_s / 2., 3.,
               np.float(patch.max() - patch.min()), np.float(patch.min())]
    errfunc = lambda p: patch.flatten() - gauss_continuous(p, w_s)
    return leastsq(errfunc, params0, xtol=0.01)


def gauss_continuous(params, w_s):
    """2D gauss function with a float center position"""
    xc, yc, width, I, bg = params
    xc = np.float(xc)
    yc = np.float(yc)
    x = np.exp(- (np.arange(0, w_s) - xc) ** 2 / width ** 2)
    y = np.exp(- (np.arange(0, w_s) - yc) ** 2 / width ** 2)
    g_patch = I * np.outer(x, y) + bg
    return g_patch.flatten()


def gauss_patch(r0, w_s):
    """
    Computes an w_s by w_s image with a
    power normalized  Gaussian peak with radial symmetry
    at its center.
    """
    x = y = np.exp(- (np.arange(w_s) - w_s // 2) ** 2 / r0 ** 2)
    A = 1. / (np.sqrt(np.pi) * r0)
    g_patch = A * np.outer(x, y)
    return g_patch


def gauss_discrete(r0, i, j, w_s):
    """
    2D gauss function with a discrete center position
    """
    i -= w_s // 2
    j -= w_s // 2
    A = 1. / (np.sqrt(np.pi) * r0)
    return A * np.exp(-(i ** 2 + j ** 2) / r0 ** 2)
