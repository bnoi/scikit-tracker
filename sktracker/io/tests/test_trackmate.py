# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sktracker import data
from sktracker.io.trackmate import trackmate_peak_import


def test_trackmate_xml_peak_import():
    trajs = trackmate_peak_import(data.trackmate_xml())
    assert trajs.x.mean().round(3) == 2.279
