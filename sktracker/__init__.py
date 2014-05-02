
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from .version import __version__

from . import data
from . import detection
from . import io
from . import trajectories
from . import tracker
from . import utils

__all__ = ['__version__',
           'set_log_level',
           'data',
           'io',
           'trajectories',
           'detection',
           'tracker',
           'utils']


def setup_log():  # pragma: no cover

    import logging

    from .utils.color_system import color
    from .utils.ipython import in_ipython

    logger = logging.getLogger(__name__)

    if not getattr(logger, 'handler_set', None):

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

        handler = logging.StreamHandler()
        formatter = logging.Formatter(logformat, "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        logger.handler_set = True


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
