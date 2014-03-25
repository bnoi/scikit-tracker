import os
from sktracker import data
from sktracker.io import StackIO
from sktracker.detection import nuclei_detector
from nose import with_setup


def setup():
    global stack_iter
    global metadata
    image_path_list = data.stack_list()

    metadata =  {"PhysicalSizeX": 0.42,
                 "PhysicalSizeY": 0.42,
                 "PhysicalSizeZ": 1.5,
                 "TimeIncrement": 3,
                 "FileName": '',
                 "Shape": [1, 1, 512, 512],
                 "DimensionOrder": "TZYX" }
    metadata['FileName'] = image_path_list[0]
    stack_io = StackIO(image_path_list=image_path_list,
                       metadata=metadata)
    im0 = stack_io.get_tif().asarray()
    correct_metadata = {'FileName': os.path.basename(image_path_list[0]),
                        'SizeX': im0.shape[2],
                        'SizeY': im0.shape[1],
                        'SizeZ': im0.shape[0],
                        'SizeT': len(image_path_list),
                        'Shape': (len(image_path_list),
                                  im0.shape[2],
                                  im0.shape[1],
                                  im0.shape[0])}
    stack_io.metadata.update(correct_metadata)
    metadata = stack_io.metadata
    stack_iter = stack_io.list_iterator()

@with_setup(setup)
def test_nuclei_detector_naive():
    parameters = {'segment_method':'naive',
                  'correction':0.2,
                  'min_z_size':0.}
    cell_positions = nuclei_detector(stack_iter(),
                                     metadata=metadata,
                                     parameters=parameters)
    assert cell_positions.shape == (19, 6)

@with_setup(setup)
def test_nuclei_detector_otsu():
    parameters = {'segment_method':'otsu',
                  'correction':1.,
                  'min_z_size':0.}
    cell_positions = nuclei_detector(stack_iter(),
                                     metadata=metadata,
                                     parameters=parameters)
    assert cell_positions.shape == (13, 6)

@with_setup(setup)
def test_nuclei_detector_none():
    parameters = {'segment_method':'naive',
                  'correction':1.,
                  'min_z_size':100.}
    cell_positions = nuclei_detector(stack_iter(),
                                     metadata=metadata,
                                     parameters=parameters)
    assert cell_positions.empty

