"""Object detection and tracking for cell biology

`scikit-tracker` is bla bla bla.

Subpackages
-----------
utils
    Utilities functions

"""

from .version import __version__

__all__ = ['__version__', 'set_log_level']


def setup_log():  # pragma: no cover

    import logging

    from .utils import color
    from .utils import in_ipython

    if in_ipython():
        logformat = '%(asctime)s' + ':'
        logformat += '%(levelname)s' + ':'
        logformat += '%(name)s' + ':'
        # logformat += '%(funcName)s' + ': '
        logformat += ' %(message)s'
    else:
        logformat = color('%(asctime)s', 'BLUE') + ':'
        logformat += color('%(levelname)s', 'RED') + ':'
        logformat += color('%(name)s', 'YELLOW') + ':'
        # logformat += color('%(funcName)s', 'GREEN') + ': '
        logformat += color(' %(message)s', 'ENDC')

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logformat, "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False


def set_log_level(loglevel):
    """
    Parameters
    ----------
    loglevel : str
        Should be DEBUG, INFO, WARNING, ERROR, CRITICAL
    """

    import logging

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):  # pragma: no cover
        raise ValueError('Invalid log level : {}'.format(loglevel))

    logger = logging.getLogger(__name__)
    logger.setLevel(numeric_level)

setup_log()
set_log_level('ERROR')
