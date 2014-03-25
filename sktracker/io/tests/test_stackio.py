from nose.tools import assert_raises

from sktracker import data
from sktracker.io import StackIO
from sktracker.io import ObjectsIO
from sktracker.io.utils import load_img_list


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

def test_stackio_image_iterator():
    fname = data.CZT_peaks()
    st = StackIO(fname, json_discovery=False)

    arr = st.get_tif().asarray(memmap=True).shape

    iterator = st.image_iterator(channel_index=0, memmap=True)
    for a in iterator():
        assert a.shape == arr[-2:]

def test_load_img_list():
    stack_list_dir = data.stack_list_dir()
    file_list = load_img_list(stack_list_dir)
    file_names = ['Stack-1.tif', 'Stack-2.tif', 'Stack-3.tif', 'Stack-4.tif']
    assert len(file_list) == len(file_names)
    for path, name in zip(file_list, file_names):
        assert path.endswith(name)

def test_stackio_list_iterator():

    metadata = {'SizeC': 1,
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

    file_list = data.stack_list()
    stackio = StackIO(image_path_list=file_list, metadata=metadata)
    stack_iter = stackio.list_iterator()

    for n, stack in enumerate(stack_iter()):
        assert stack.shape == (5, 172, 165)
    assert n == 3

def test_stackio_get_tif_from_list():
    images_list = data.stack_list()
    st = StackIO(image_path_list=images_list)
    assert st.get_tif_from_list(3).asarray().shape == (5, 172, 165)
