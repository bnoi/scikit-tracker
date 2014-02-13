__all__ = ['print_progress']

import sys

def print_progress(progress):
    """Display a progress bar filled with a variable value. print_progress
    also works under IPython notebook.

    Parameters
    ----------
    progress: int
        Variable value use to fill the progress bar. Should be between 0
        and 100.

    Returns
    -------
    None. Display the progress bar.

    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.montage import montage2d
    >>> arr_in = np.arange(3 * 2 * 2).reshape(3, 2, 2)
    >>> arr_in  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1],
            [ 2,  3]],
           [[ 4,  5],
            [ 6,  7]],
           [[ 8,  9],
            [10, 11]]])
    >>> arr_out = montage2d(arr_in)
    >>> arr_out.shape
    (4, 4)
    >>> arr_out
    array([[  0. ,   1. ,   4. ,   5. ],
           [  2. ,   3. ,   6. ,   7. ],
           [  8. ,   9. ,   5.5,   5.5],
           [ 10. ,  11. ,   5.5,   5.5]])
    >>> arr_in.mean()
    5.5
    >>> arr_out_nonsquare = montage2d(arr_in, grid_shape=(1, 3))
    >>> arr_out_nonsquare
    array([[  0.,   1.,   4.,   5.,   8.,   9.],
           [  2.,   3.,   6.,   7.,  10.,  11.]])
    >>> arr_out_nonsquare.shape
    (2, 6)

    """

    # If process is finished
    if percent == -1:
        sys.stdout.write("\r" + " " * 80 + "\r\r")
        sys.stdout.flush()
        return

    # Size of the progress bar
    size = 50

    # Compute current progress
    progress = (percent + 1) * size / 100

    # Build progress bar
    bar = "["
    for i in range(int(progress - 1)):
        bar += "="
    bar += ">"
    for i in range(int(size - progress)):
        bar += " "
    bar += "]"

    # Write progress bar
    sys.stdout.write("\r%d%% " % (percent + 1) + bar)
    sys.stdout.flush()
