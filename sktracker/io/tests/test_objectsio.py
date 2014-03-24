import os

from nose import with_setup

from  sktracker import data


from sktracker.io import objectsio, validate_metadata

def test_from_store():

    store_path = data.sample_h5()
    oio = objectsio.ObjectsIO.from_h5(store_path)
    assert validate_metadata(oio.metadata)

