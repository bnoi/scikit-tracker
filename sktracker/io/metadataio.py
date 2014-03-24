import os
import json
import logging

log = logging.getLogger(__name__)

from . import TiffFile
from . import OMEModel

__all__ = ['get_metadata']


def get_metadata(filename, json_discovery=False):
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

    tf = TiffFile(filename)

    axes = tf.series[0]['axes']
    shape = tf.series[0]['shape']

    md['Shape'] = shape
    md['DimensionOrder'] = axes

    if tf.is_imagej or tf.is_ome:

        for dim_label in ['T', 'C', 'Z', 'Y', 'X']:
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
                log.info('Load metadata from %s' % metadata_path)
                metadata = json.load(open(metadata_path))
            except:
                pass

    return metadata

def validate_metadata(metadata,
                      keys=['DimensionOrder',
                            'Shape',
                            'FileName']):
    err = []
    for key in keys:
        if not key in metadata:
            err.append(key)
    if len(err):
        raise ValueError('metadata missing the following key(s):\n'
                         '{}'.format('\n'.join([key for key in err])))
    return True
