
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
log = logging.getLogger(__name__)

from .trajectories import Trajectories
try:
    from . import draw
    __all__ = ['Trajectories', 'draw']
except ImportError:
    # log.warning('''Looks like matplotlib can't be imported,'''
    #             '''drawing won't be available ''')
    __all__ = ['Trajectories']
