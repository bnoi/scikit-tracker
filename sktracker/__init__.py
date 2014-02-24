"""Object detection and tracking for cell biology

`scikit-learn` is bla bla bla.

Subpackages
-----------
utils
    Utilities functions

"""

import logging

try:
    from .version import __version__
except ImportError: # pragma: no cover
    __version__ = "dev" # pragma: no cover

def setup_log(): # pragma: no cover

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
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

setup_log()
