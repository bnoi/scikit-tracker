import os

from sktracker import data
from sktracker.io import get_metadata


def test_get_metadata():
    fname = data.sample()
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
