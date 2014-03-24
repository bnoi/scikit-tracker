from nose.tools import assert_raises

from sktracker import data
from sktracker.io import StackIO


def test_stackio_from_tif_file():

    st = StackIO.from_tif_file(data.CZT_peaks())

    # Test metadata
    true_metadata = {'SizeC': 1,
                     'TimeIncrement': 10.0,
                     'DimensionOrder': ['C', 'T', 'Z', 'Y', 'X'],
                     'SizeT': 4,
                     'AcquisitionDate': '2014-03-24T11:25:14',
                     'SizeX': 56,
                     'SizeY': 48,
                     'SizeZ': 4,
                     'PhysicalSizeY': 0.065,
                     'PhysicalSizeX': 0.065,
                     'Shape': (1, 4, 4, 48, 56),
                     'PhysicalSizeZ': 1.0}

    guessed_metadata = st.metadata
    guessed_metadata.pop("FileName")

    assert guessed_metadata == true_metadata

def test_stackio_from_objectsio():
    pass

def test_stackio_get_data():
    st = StackIO.from_tif_file(data.CZT_peaks())
    arr = st.get_data()
    assert arr.shape == (1, 4, 4, 48, 56)
