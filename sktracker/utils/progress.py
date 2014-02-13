__all__ = ['print_progress']

import sys


def print_progress(progress):
    """Display a progress bar filled with a variable value. print_progress
    also works under IPython notebook.

    Se `progress` to -1 to remove the progress bar.

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
    >>> import time
    >>> from sktracker.utils import print_progress

    >>> n = 5
    >>> for i in range(n):
    >>>     time.sleep(1)

    >>>     print_progress((i + 1) * 100 / n)
    100% [=================================================>]
    >>> print_progress(-1)

    """

    # If process is finished
    if progress == -1:
        sys.stdout.write("\r" + " " * 80 + "\r\r")
        sys.stdout.flush()
        return

    # Size of the progress bar
    size = 50

    # Compute current progress
    progress_bar = (progress) * size / 100

    # Build progress bar
    bar = "["
    for i in range(int(progress_bar - 1)):
        bar += "="
    bar += ">"
    for i in range(int(size - progress_bar)):
        bar += " "
    bar += "]"

    # Write progress bar
    sys.stdout.write("\r%d%% " % (progress) + bar)
    sys.stdout.flush()
