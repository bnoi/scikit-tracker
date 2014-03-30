from numpy.testing import assert_array_almost_equal

import numpy as np

from sktracker import data
from sktracker.io import StackIO
from sktracker.detection import cell_boundaries_detector


def test_cell_boundaries_detector():

    # Fake to only detect the first time stamp
    # to make tests faster

    st = StackIO(data.TC_BF_cells())
    data_iterator = [list(st.image_iterator(position=-3)())[0]]

    metadata = st.metadata
    metadata['SizeT'] = 1

    parameters = {'object_height': 3,
                  'minimal_area': 160}

    shapes = cell_boundaries_detector(data_iterator, st.metadata,
                                      show_progress=True,
                                      parameters=parameters)

    real_shapes = np.array([[5.529290429042903909e+00, 7.725527184297377836e+00,
                             -1.109566958016608318e+00, 1.057975329135689790e+01,
                             7.965464600887037783e+00, 0.000000000000000000e+00]])

    assert_array_almost_equal(shapes, real_shapes)


def test_cell_boundaries_detector_no_shapes():

    # Fake to only detect the first time stamp
    # to make tests faster

    st = StackIO(data.CZT_peaks())
    data_iterator = [list(st.image_iterator(position=-3, channel_index=0)())[0]]

    metadata = st.metadata
    metadata['SizeT'] = 1

    parameters = {'object_height': 1e-6,
                  'minimal_area': 160}

    shapes = cell_boundaries_detector(data_iterator, metadata,
                                      show_progress=True,
                                      parameters=parameters)

    assert shapes.empty is True
