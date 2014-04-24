# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import tempfile

from sktracker import data
from sktracker.io import StackIO
from sktracker.io import ObjectsIO

from sktracker.detection import peak_detector
from sktracker.io import validate_metadata


def test_objectsio():

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
                          show_progress=True,
                          parameters=parameters)

    oio = ObjectsIO(st.metadata, store_path="test.h5", base_dir=tempfile.gettempdir())
    oio["detected"] = peaks
    keys_ok = (oio.keys() == ['detected', 'metadata'] or oio.keys() == ['/detected', '/metadata'])
    print(oio.keys())
    print(oio["detected"].shape)
    assert keys_ok and (oio["detected"].shape == (28, 6))


def test_oio_metadata():

    store_path = data.sample_h5_temp()
    oio = ObjectsIO.from_h5(store_path, base_dir=tempfile.gettempdir())
    oio.metadata['test'] = 0
    assert 'test' in oio.metadata.keys()
    reloaded = ObjectsIO.from_h5(store_path, base_dir=tempfile.gettempdir())
    assert 'test' in reloaded.metadata.keys()


def test_from_h5():

    store_path = data.sample_h5_temp()
    oio = ObjectsIO.from_h5(store_path, base_dir=tempfile.gettempdir())
    assert validate_metadata(oio.metadata)


def test_from_trackmate_xml():
    xml_fname = data.trackmate_xml_temp()
    oio = ObjectsIO.from_trackmate_xml(xml_fname)
    assert oio['trajs'].shape == (91, 6)
