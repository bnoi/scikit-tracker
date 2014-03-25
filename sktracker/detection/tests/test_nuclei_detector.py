import os
from sktracker import data
from sktracker.io import StackIO
from sktracker.detection import nuclei_detector as nud
from nose import with_setup

def setup():
    global stack_iter
    global metadata
    image_path_list = data.stack_list()
    metadata = nud.DEFAULT_METADATA.copy()
    metadata['FileName'] = image_path_list[0]
    stack_io = StackIO(image_path_list=image_path_list,
                       metadata=metadata)
    im0 = stack_io.get_tif().asarray()
    correct_metadata = {'FileName':os.path.basename(image_path_list[0]),
                        'SizeX':im0.shape[2],
                        'SizeY':im0.shape[1],
                        'SizeZ':im0.shape[0],
                        'SizeT':len(image_path_list)}
    stack_io.metadata.update(correct_metadata)
    metadata = stack_io.metadata
    stack_iter = stack_io.list_iterator()

@with_setup(setup)
def test_nuclei_detector_naive():
    parameters = {'segment_method':'naive',
                  'correction':0.2,
                  'min_z_size':0.}
    cell_positions = nud.nuclei_detector(stack_iter(),
                                         metadata=metadata,
                                         parameters=parameters)
    assert cell_positions.shape == (19, 5)

@with_setup(setup)
def test_nuclei_detector_otsu():
    parameters = {'segment_method':'otsu',
                  'correction':1.,
                  'min_z_size':0.}
    cell_positions = nud.nuclei_detector(stack_iter(),
                                         metadata=metadata,
                                         parameters=parameters)
    assert cell_positions.shape == (13, 5)

@with_setup(setup)
def test_nuclei_detector_none():
    parameters = {'segment_method':'naive',
                  'correction':1.,
                  'min_z_size':100.}
    cell_positions = nud.nuclei_detector(stack_iter(),
                                         metadata=metadata,
                                         parameters=parameters)
    assert cell_positions.empty

