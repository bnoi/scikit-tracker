import os
import json
import logging

log = logging.getLogger(__name__)

from . import TiffFile
from . import OMEModel

__all__ = []


def get_metadata(filename, json_discovery=False, base_dir=None):
    """Get image file metadata
    Metadata will be retrieved from TIFF IFD comments. OME is automatically
    detected. Additionnaly a file called metadata.json can be in the same
    directory or in the parent directory will be read to initialize metadata.

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

    if base_dir:
        tf = TiffFile(os.path.join(base_dir, filename))
    else:
        tf = TiffFile(filename)

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
        xml_metadata = tf[0].tags['image_description'].value.decode()
        ome = OMEModel(xml_metadata)
        md.update(ome.get_metadata())

    # if tf.is_micromanager:
        # pass
        # Informations can be found here: tf.micromanager_metadata

    if json_discovery:
        json_metadata = _get_from_metadata_json(filename)
        md.update(json_metadata)

    md["FileName"] = filename

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
    candidats = [os.path.join(file_dir, '..', 'metadata.json'),
                 os.path.join(file_dir, 'metadata.json')]

    for metadata_path in candidats:
        if os.path.isfile(metadata_path):
            try:
                metadata = json.load(open(metadata_path))
            except:
                pass

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
