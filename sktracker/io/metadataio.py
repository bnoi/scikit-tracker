# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import os
import json
import ast
import logging
from collections import OrderedDict

import numpy as np

log = logging.getLogger(__name__)

from . import TiffFile
from .ome import OMEModel

__all__ = []

METADATA_TYPE = {'SizeT': int,
                 'SizeZ': int,
                 'SizeC': int,
                 'SizeY': int,
                 'SizeX': int,
                 'SizeI': int,
                 'PhysicalSizeX': float,
                 'PhysicalSizeY': float,
                 'PhysicalSizeZ': float,
                 'TimeIncrement': float,
                 'Shape': (list, tuple),
                 'DimensionOrder': (list, tuple, str),
                 'Channels': (list, tuple),
                 'AcquisitionDate': str,
                 'unique_id': str,
                 'FileName': str}


class OIOMetadata(OrderedDict):
    '''
    A subclass of OrderedDict with a modified `__setitem__`, such that
    any modification to the metadata is copied to the `h5` file
    '''
    def __init__(self, metadata_dict, objectsio):
        self.objectsio = objectsio
        OrderedDict.__init__(self, metadata_dict)
        self.objectsio['metadata'] = self
        self._check_data_type()

    def __setitem__(self, key, value):

        OrderedDict.__setitem__(self, key, value)
        self.objectsio['metadata'] = self

    def _check_data_type(self):
        """"Check for basic data type. If data type does not match then try to catch.
        """

        for k, v in METADATA_TYPE.items():
            if k in self.keys():
                if not isinstance(self[k], v):
                    try:
                        if type(v).__name__ in ['list', 'tuple']:
                            self[k] = ast.literal_eval(self[k])
                        else:
                            if v.__name__ == 'int':
                                self[k] = v(np.round(float(self[k])))
                    except:
                        msg = "Metadata contains wrong data type '{}'' has type {}, should be {}"
                        raise ValueError(msg.format(k, type(self[k]), v))


def get_metadata(filename, json_discovery=False, base_dir=None):
    """Get image file metadata. Metadata will be retrieved from TIFF IFD comments. OME is
    automatically detected. Additionnaly a file called metadata.json can be in the same directory or
    in the parent directory will be read to initialize metadata.

    Parameters
    ----------
    filename: str
        Filename of the image

    Returns
    -------
    metadata: dict
        A dict with all metadata retrieved from the Tiff file

    """
    md = {}
    md["FileName"] = filename

    abs_filename = None

    if base_dir:
        abs_filename = os.path.join(base_dir, filename)
    else:
        abs_filename = filename

    tf = TiffFile(abs_filename)

    axes = tf.series[0]['axes']
    shape = tf.series[0]['shape']

    md['Shape'] = shape
    md['DimensionOrder'] = axes

    if tf.is_imagej or tf.is_ome:

        for dim_label in md['DimensionOrder']:
            try:
                dim_id = axes.index(dim_label)
                md["Size" + dim_label] = shape[dim_id]
            except:
                md["Size" + dim_label] = 1

    if tf.is_ome:
        xml_metadata = tf[0].tags['image_description'].value.decode(errors='ignore')
        ome = OMEModel(xml_metadata)
        md.update(ome.get_metadata())

    # if tf.is_micromanager:
        # pass
        # Informations can be found here: tf.micromanager_metadata

    if json_discovery:
        json_metadata = _get_from_metadata_json(abs_filename)
        md.update(json_metadata)

    del tf
    import gc
    gc.collect()

    return md


def _get_from_metadata_json(filename):
    """Get metadata from json file
    metadata.json file will be read in the same or the parent directory of the
    file `filename`.

    Parameters
    ----------
    filename: str
        Filename of the image

    Returns
    -------
    metadata: dict
        A dict with all metadata retrieved from the metadata.json

    """
    metadata = {}

    file_dir = os.path.dirname(filename)
    candidats = [os.path.join(file_dir, '..', '..', 'metadata.json'),
                 os.path.join(file_dir, '..', 'metadata.json'),
                 os.path.join(file_dir, 'metadata.json')]

    for metadata_path in candidats:
        if os.path.isfile(metadata_path):
            metadata = json.load(open(metadata_path))

    return metadata


def validate_metadata(metadata, keys=[]):
    err = []
    for key in keys:
        if key not in metadata.keys():
            err.append(key)
    if len(err):
        raise ValueError('metadata missing the following key(s):\n'
                         '{}'.format('\n'.join([key for key in err])))
    return True
