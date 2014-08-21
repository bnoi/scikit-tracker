# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import tempfile

import numpy as np
import pandas as pd

from sktracker import data
from sktracker.io import StackIO
from sktracker.io import ObjectsIO

from sktracker.io import validate_metadata


def test_objectsio():

    fname = data.CZT_peaks()
    st = StackIO(fname, json_discovery=False)

    oio = ObjectsIO(st.metadata, store_path="test.h5", base_dir=tempfile.gettempdir())

    oio["detected"] = pd.DataFrame(np.random.random((5, 100)))
    keys_ok = (oio.keys() == ['detected', 'metadata'] or oio.keys() == ['/detected', '/metadata'])

    assert keys_ok and (oio["detected"].shape == (5, 100))


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

    store_path = data.sample_h5_temp()
    oio = ObjectsIO.from_h5(store_path)
    assert validate_metadata(oio.metadata)


def test_from_stackio():

    fname = data.CZT_peaks_temp()
    st = StackIO(fname, json_discovery=False)

    oio = ObjectsIO.from_stackio(st)
    assert oio.keys() == ['/metadata']


def test_oio_init():

    store_path = data.sample_h5_temp()
    metadata = {'FileName': store_path}
    oio = ObjectsIO(metadata)
    assert oio.store_path == store_path

    # Test no metadata provided without base_dir

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path)

    good_md = {'SizeZ': 23.0,
               'SizeT': 5.0,
               'DimensionOrder': 'TZYX',
               'PysicalSizeY': 0.43,
               'PysicalSizeX': 0.43,
               'FileName': 'sample.ome.tif',
               'Type': 'unint16',
               'TimeIncrement': 3.0,
               'Shape': (512, 512, 23, 5),
               'SizeY': 512.0,
               'PysicalSizeZ': 1.5,
               'SizeX': 512.0}

    assert good_md == dict(oio['metadata'])

    # Test no metadata provided with base_dir

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path, base_dir=os.path.dirname(store_path))

    assert good_md == dict(oio['metadata'])


def test_oio_delitem():

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path)

    assert oio.keys() == ['/metadata', '/objects']
    del oio['metadata']
    assert oio.keys() == ['/objects']


def test_oio_get_all_items():

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path)

    assert [key for key, values in oio.get_all_items()] == ['metadata', 'objects']


def test_clean_store_file():

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path, clean_store=True)

    before = os.path.getsize(oio.store_path)
    oio["/objects"] = oio["/objects"].copy()
    # No cleanup here so filesize will increase
    after = os.path.getsize(oio.store_path)

    assert before < after

    store_path = data.sample_h5_temp()
    oio = ObjectsIO(store_path=store_path, clean_store=True)

    before = os.path.getsize(oio.store_path)
    oio["/objects"] = oio["/objects"].copy()
    oio.clean_store_file()
    after = os.path.getsize(oio.store_path)

    assert before == after
