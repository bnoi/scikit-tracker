# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from sktracker.utils.dict import sanitize_dict
from sktracker.utils.dict import guess_values_type


def test_sanitize_dict():

    d = dict(a=1, b=['r', 8, 9])
    assert sanitize_dict(d) == {'a': '1', 'b': "['r', 8, 9]"}


def test_guess_values_type():

    d = {'a': '1', 'b': '["r", 8, 9]'}
    assert guess_values_type(d) == {'a': 1.0, 'b': ['r', 8, 9]}
