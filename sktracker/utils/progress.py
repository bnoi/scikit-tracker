
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import sys

__all__ = []


def print_progress(progress, message=None, out=None):
    """Display a progress bar filled with a variable value. print_progress
    also works under IPython notebook.

    Set `progress` to -1 to remove the progress bar.

    Parameters
    ----------
    progress: int
        Variable value use to fill the progress bar. Should be between 0
        and 100.
    out: OutStream
        Where to stream progress bar. None will redirect output to `sys.stdout`.

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

    if out is None:
        out = sys.stdout

    # If process is finished
    if progress == -1:
        out.write("\r" + " " * 80 + "\r\r")
        out.flush()
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

    if message:
        bar = " ".join([bar, message])

    # Write progress bar
    bar_str = "\r%d%% " % (progress) + bar
    out.write(bar_str)
    out.flush()


def progress_apply(g, func, out=None, *args, **kwargs):
    """Add to :class:`pandas.DataFrameGroupBy` a progress bar.

    From http://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations-python.

    Parameters
    ----------
    g : :class:`pandas.DataFrameGroupBy`
    func : function

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from sktracker.utils import progress_apply

    >>> df = pd.DataFrame(np.random.choice(range(100), (1000000, 4)), columns=['A', 'B', 'C', 'D'])
    >>> gp = df.groupby('A')
    >>> progress_apply(gp, lambda x: np.sqrt((x**2) / 1e99))
    >>> # See the progress bar
    """

    if out is None:
        out = sys.stdout

    n = len(g)

    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            progress = wrapper.count * 100 / n
            print_progress(progress, out=out)
            wrapper.count += 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper

    logged_func = logging_decorator(func)
    res = g.apply(logged_func)
    print_progress(-1, out=out)
    return res
