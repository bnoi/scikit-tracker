import os
import logging

from .metadataio import get_metadata
from . import TiffFile

log = logging.getLogger(__name__)

__all__ = ['StackIO']

class StackIO:
    """StackIO is designed to deal with Input/Output images. It can retrieve all
    kind of metadata with various methods. It also allows fast and efficient way
    to get image data (in memory or via an iterator).

    """

    def __init__(self, tif_name=None,
                 tif_list=None,
                 stream_url=None,
                 objectios=None,
                 base_dir=None,
                 json_discovery=False):
        """
        """

        if tif_name:
            self._init_single_tif(tif_name, base_dir, json_discovery)
        elif tif_list:
            self._init_multiple_tif(tif_list, base_dir, json_discovery)
        elif stream_url:
            self._init_stream(stream_url)
        elif objectios:
            self._init_objectsio(objectios)

    @property
    def image_path(self):
        if self.base_dir:
            return os.path.join(self.base_dir, self.metadata['FileName'])
        else:
            return self.metadata['FileName']


    @classmethod
    def from_tif_file(cls, tif_name, base_dir=None, json_discovery=False):
        """Load images from Tiff file.

        Parameters
        ----------
        tif_name : str
            Path to image file.
        base_dir : path or None
            Specify a root directory relative to `tif_name`.
        json_discovery : bool
            Find metadata in metadata.json files.

        """
        return cls(tif_name=tif_name, base_dir=None, json_discovery=json_discovery)

    @classmethod
    def from_tif_list(cls, tif_list):
        """
        """
        pass

    @classmethod
    def from_stream(cls, stream_url):
        """
        """
        pass

    @classmethod
    def from_objectsio(cls, objectios):
        """Load images and metadata from `sktracker.io.ObjectsIO`

        Parameters
        ----------
        objectios : object
            `sktracker.io.ObjectsIO` instance.
        """
        return cls(objectios=objectios)


    def _init_single_tif(self, tif_name, base_dir, json_discovery):
        if os.path.isabs(tif_name) and base_dir:
            tif_name = os.path.relpath(base_dir, tif_name)

        self.metadata = get_metadata(tif_name, json_discovery)
        self.base_dir = base_dir

    def _init_multiple_tif(self, tif_list, json_discovery):
        pass

    def _init_stream(self, stream_url):
        pass

    def _init_objectsio(self, objectios):
        self.metadata = objectios.metadata
        self.base_dir = objectios.base_dir

    def get_data(self, key=None, series=None, memmap=False):
        """Retrieve image data as array.

        Parameters
        ----------
        key : int, slice, or sequence of page indices
            Defines which pages to return as array.
        series : int
            Defines which series of pages to return as array.
        memmap : bool
            If True, use numpy.memmap to read arrays from file if possible.

        """

        tf = TiffFile(self.image_path)
        return tf.asarray(key=key, series=series, memmap=memmap)
