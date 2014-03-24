import os

import sktracker
from sktracker.io import get_metadata

data_dir = sktracker.data.path

def test_get_metadata():
    fname = os.path.join(data_dir, "sample.ome.tif")
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

    assert real_metadata == get_metadata(fname)
