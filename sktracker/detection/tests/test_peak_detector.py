
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from sktracker import data
from sktracker.io import StackIO
from sktracker.detection import peak_detector


def test_peak_detector():

    fname = data.CZT_peaks()
    st = StackIO(fname, json_discovery=False)

    data_iterator = st.image_iterator(channel_index=0)

    parameters = {'w_s': 0.7,
                  'peak_radius': 0.2,
                  'threshold': 27,
                  'max_peaks': 4
                  }

    peaks = peak_detector(data_iterator(),
                          st.metadata,
                          parallel=True,
                          show_progress=False,
                          parameters=parameters)

    assert peaks.shape == (28, 6)


def test_peak_detector_no_peaks():

    fname = data.CZT_peaks()
    st = StackIO(fname, json_discovery=False)

    data_iterator = st.image_iterator(channel_index=0)

    parameters = {'w_s': 0.7,
                  'peak_radius': 0.2,
                  'threshold': 300,
                  'max_peaks': 4}

    peaks = peak_detector(data_iterator(),
                          st.metadata,
                          parallel=True,
                          show_progress=False,
                          parameters=parameters)

    assert peaks.empty is True
