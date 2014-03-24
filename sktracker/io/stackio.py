import os
import logging

log = logging.getLogger(__name__)

__all__ = ['StackIO']

class StackIO:
    """StackIO is designed to deal with Input/Output images. It can retrieve all
    kind of metadata with various methods. It also allows fast and efficient way
    to get image data (in memory or via an iterator).

    """

    def __init__(self, tif_name=None, tif_list=None, stream_url=None):
        """
        """

        if tif_name:
            self._init_single_tif(tif_name)
        elif tif_list:
            self._init_multiple_tif(tif_list)
        elif stream_url:
            self._init_stream(stream_url)

    @classmethod
    def from_tif_file(cls, tif_name):
        """Load images from Tiff file.

        Parameters
        ----------
        tif_name : str
            Path to image file.

        """
        return cls(tif_name=tif_name)

    @classmethod
    def from_tif_list(cls, tif_list):
        pass

    @classmethod
    def from_stream(cls, stream_url):
        pass

    def _init_single_tif(self, tif_name):
        self.tif_name = tif_name

    def _init_multiple_tif(self, tif_list):
        pass

    def _init_stream(self, stream_url):
        pass

