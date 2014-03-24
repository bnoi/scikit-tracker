import os

from sktracker.io import get_metadata

current_dir = os.path.dirname(os.path.realpath(__file__))

def test_get_metadata():
    fname = os.path.join(current_dir, "sample.ome.tif")
    real_metadata = {'PhysicalSizeY': 0.065,
                     'SizeC': 2,
                     'SizeZ': 8,
                     'SizeT': 20,
                     'PhysicalSizeX': 0.065,
                     'SizeY': 20,
                     'SizeX': 50,
                     'PhysicalSizeZ': 0.3,
                     'DimensionOrder': ['T', 'Z', 'C', 'Y', 'X'],
                     'AcquisitionDate': '2014-02-24T15:29:53',
                     'Shape': (20, 8, 2, 20, 50)}

    assert real_metadata == get_metadata(fname)
