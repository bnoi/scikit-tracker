# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from sktracker.utils.sort import natural_keys

def test_naturalkeys():

    alist = ["something1", "something12", "something17", "something2"]
    alist.sort(key=natural_keys)
    assert alist == ['something1', 'something2', 'something12', 'something17']
