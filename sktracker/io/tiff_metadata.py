import logging

log = logging.getLogger(__name__)

from . import TiffFile
from . import OMEModel

__all__ = ['get_metadata_from_tiff']


def get_metadata_from_tiff(tf):
    """Get Tiff file metadata.

    Parameters
    ----------
    tf: str
        Filename to Tiff file

    Returns
    -------
    metadata: dict
        A dict with all metadata retrieved from the Tiff file

    """
    md = {}

    tf = TiffFile(tf)

    axes = tf.series[0]['axes']
    shape = tf.series[0]['shape']

    md['shape'] = shape
    md['axes'] = axes

    if tf.is_imagej or tf.is_ome:

        for dim_label in ['T', 'C', 'Z', 'Y', 'X']:
            try:
                dim_id = axes.index(dim_label)
                md[dim_label.lower()] = shape[dim_id]
            except:
                md[dim_label.lower()] = 1

    if tf.is_ome:
        xml_metadata = tf[0].tags['image_description'].value.decode()
        ome = OMEModel(xml_metadata)
        md.update(ome.get_metadata())

    # if tf.is_micromanager:
        # pass
        # Informations can be found here: tf.micromanager_metadata

    return md
