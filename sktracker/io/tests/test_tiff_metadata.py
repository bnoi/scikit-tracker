import os

from sktracker.io import get_metadata_from_tiff

current_dir = os.path.dirname(os.path.realpath(__file__))

def test_get_metadata_from_tiff():
    fname = os.path.join(current_dir, "sample.ome.tif")
    real_metadata = {'PhysicalSizeY': 0.065,
                     'c': 2,
                     'z': 8,
                     't': 20,
                     'PhysicalSizeX': 0.065,
                     'y': 20,
                     'x': 50,
                     'PhysicalSizeZ': 0.3,
                     'axes': ['T', 'Z', 'C', 'Y', 'X'],
                     'acquisition_date': '2014-02-24T15:29:53',
                     'shape': (20, 8, 2, 20, 50)}

    assert real_metadata == get_metadata_from_tiff(fname)
