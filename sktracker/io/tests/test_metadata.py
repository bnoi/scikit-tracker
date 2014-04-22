
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from nose.tools import assert_raises

from sktracker import data
from sktracker.io import get_metadata
from sktracker.io import validate_metadata


def test_get_metadata():
    fname = data.sample_ome()
    real_metadata = {'PhysicalSizeY': 0.065,
                     'SizeC': 2,
                     'SizeZ': 8,
                     'SizeT': 20,
                     'PhysicalSizeX': 0.065,
                     'SizeY': 20,
                     'SizeX': 50,
                     'PhysicalSizeZ': 0.8,
                     'DimensionOrder': ['T', 'Z', 'C', 'Y', 'X'],
                     'AcquisitionDate': '2014-02-24T15:29:53',
                     'Shape': (20, 8, 2, 20, 50)}

    guessed_metadata = get_metadata(fname, json_discovery=True)
    guessed_metadata.pop("FileName", None)

    assert real_metadata == guessed_metadata


def test_invalidate_metadata():

    bad_metadata = {'SizeC': 2, 'SizeZ': 8}
    assert_raises(ValueError, validate_metadata, bad_metadata, ['DimensionOrder'])


def test_validate_metadata():

    good_metadata = {'PhysicalSizeY': 0.065,
                     'SizeC': 2,
                     'SizeZ': 8,
                     'SizeT': 20,
                     'PhysicalSizeX': 0.065,
                     'SizeY': 20,
                     'SizeX': 50,
                     'PhysicalSizeZ': 0.8,
                     'DimensionOrder': ['T', 'Z', 'C', 'Y', 'X'],
                     'AcquisitionDate': '2014-02-24T15:29:53',
                     'Shape': (20, 8, 2, 20, 50),
                     'FileName': '../../data/sample.ome.tif'}

    default_good = validate_metadata(good_metadata)
    extra_good = validate_metadata(good_metadata,
                                   keys=['PhysicalSizeZ',
                                         'DimensionOrder',
                                         'AcquisitionDate'])
    assert default_good and extra_good
