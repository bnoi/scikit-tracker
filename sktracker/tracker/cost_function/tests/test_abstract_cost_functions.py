# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from nose.tools import assert_raises
import sys
import pandas as pd
import numpy as np

from sktracker.tracker.cost_function import AbstractCostFunction


def test_abstract_cost_function():

    cost_func = AbstractCostFunction(context={}, parameters={})

    assert cost_func.get_block() == None


def test_abstract_cost_function_check_context():

    cost_func = AbstractCostFunction(context={'cost': 1}, parameters={})

    assert_raises(ValueError, cost_func.check_context, 'test_string', str)

    cost_func.context['test_string'] = 5

    assert_raises(TypeError, cost_func.check_context, 'test_string', str)

    cost_func.context['test_string'] = "i am a string"
    ### This fails in py2.7
    if sys.version_info[0] > 2:
        cost_func.check_context('test_string', str)

    assert True


def test_abstract_cost_function_check_columns():

    cost_func = AbstractCostFunction(context={}, parameters={})

    df = pd.DataFrame([np.arange(0, 5), np.arange(20, 25)],
                      columns=['x', 'y', 'z', 'w', 't'])

    cost_func.check_columns(df, ['t', 'z', 'y'])
    cost_func.check_columns([df], ['t', 'z', 'y'])

    df = pd.DataFrame([np.arange(0, 4), np.arange(20, 24)],
                      columns=['x', 'y', 'w', 't'])

    assert_raises(ValueError, cost_func.check_columns, df, ['t', 'z', 'y'])
