from nose.tools import assert_raises

from sktracker import data
from sktracker.io import StackIO
from sktracker.io import ObjectsIO


def test_stackio_from_tif_file():

    st = StackIO(data.CZT_peaks(), json_discovery=False)

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
    oio = ObjectsIO.from_h5(data.sample_h5())
    st = StackIO.from_objectsio(oio)

    true_metadata = {'PysicalSizeY': 0.43,
                     'PysicalSizeX': 0.43,
                     'PysicalSizeZ': 1.5,
                     'TimeIncrement': 3.0,
                     'Shape': (512, 512, 23, 5),
                     'SizeT': 5,
                     'Type': 'unint16',
                     'FileName': 'sample.ome.tif',
                     'DimensionOrder': 'TZYX',
                     'SizeZ': 23,
                     'SizeY': 512,
                     'SizeX': 512}

    guessed_metadata = st.metadata

    assert guessed_metadata == true_metadata


def test_stackio_get_data():
    st = StackIO(data.CZT_peaks())
    tf = st.get_tif()
    arr = tf.asarray(memmap=True)
    assert arr.shape == (1, 4, 4, 48, 56)
