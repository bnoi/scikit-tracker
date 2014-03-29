__all__ = []


def in_ipython():
    """Test if current python process is an IPython process or not.

    Returns
    -------
    True wether current process is IPython, False in the other case.
    """
    try:
        __IPYTHON__
    except NameError:
        return False
    else:
        return True  # pragma: no cover
