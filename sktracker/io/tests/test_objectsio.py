import os

from nose import with_setup

from  sktracker import data


from sktracker.io import objectsio

def test_from_store():

    store_path = data.sample_h5()

    