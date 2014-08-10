# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import pandas as pd
from functools import wraps


def trajs_measure(method, *args, **kwargs):
    """
    """
    @wraps(method)
    def new_method(*args, **kwargs):
        trajs = args[0]
        measure_ = method(*args, **kwargs).sortlevel(['t_stamp', 'label'])
        measure = pd.DataFrame.from_dict({method.__name__: measure_.values.ravel(),
                                          't': trajs.t})
        measure.set_index(trajs.index)
        return measure.sortlevel(['t_stamp', 'label'])

    return new_method


def p2p_measure(method, *args, **kwargs):
    '''

    '''
    @wraps(method)
    def new_method(*args, **kwargs):
        measure = method(*args, **kwargs)
        measure.name = method.__name__
        return measure
    return new_method


def segment_measure(method, *args, **kwargs):
    '''
    '''
    return method


def sliding_measure(method, *args, **kwargs):
    '''
    '''
    return method
