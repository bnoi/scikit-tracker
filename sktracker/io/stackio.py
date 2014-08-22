
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import sys
import os
import logging

import numpy as np

from .metadataio import get_metadata
from . import TiffFile

log = logging.getLogger(__name__)

__all__ = []


class StackIO(object):
    """StackIO is designed to deal with Input/Output images
    It can retrieve all kind of metadata with various methods. It also allows fast and
    efficient way to get image data (in memory or via an iterator.

    Parameters
    ----------
    image_path : str or None
    image_path_list : list or None
    base_dir : path or None
        Specify a root directory relative to `image_path`.
    json_discovery : bool
        Find metadata in metadata.json files

    """

    def __init__(self,
                 image_path=None,
                 image_path_list=None,
                 metadata=None,
                 base_dir=None,
                 json_discovery=False):

        self.base_dir = base_dir
        if image_path_list:
            image_path = image_path_list[0]

        if metadata is not None:
            self.metadata = metadata
            if image_path is not None:
                self.metadata['FileName'] = image_path
        else:
            self.metadata = get_metadata(image_path, json_discovery,
                                         base_dir=self.base_dir)
            log.info('Getting metadata from TIFF file')

        if image_path_list:
                self.metadata['SizeT'] = len(image_path_list)
                if self.metadata['DimensionOrder'][0] != 'T':
                    self.metadata['Shape'] = ((len(image_path_list),)
                                              + tuple(self.metadata['Shape']))
                    self.metadata['DimensionOrder'] = 'T'+''.join(self.metadata['DimensionOrder'])
        self._image_path_list = image_path_list

    @property
    def image_path_list(self):
        if not self._image_path_list:
            return
        if self.base_dir:
            return [os.path.join(self.base_dir, image)
                    for image in self._image_path_list]
        else:
            return self._image_path_list

    @property
    def image_path(self):
        if self.base_dir:
            return os.path.join(self.base_dir, self.metadata['FileName'])
        else:
            return self.metadata['FileName']

    @classmethod
    def from_objectsio(cls, objectsio):
        """Load images and metadata from :class:`sktracker.io.ObjectsIO`

        Parameters
        ----------
        objectsio : :class:`sktracker.io.ObjectsIO`
        """

        return cls(image_path=objectsio.image_path, metadata=objectsio.metadata)

    def get_tif(self, multifile=True):
        """Get TiffFile instance.

        Returns
        -------
        tf : :class:`sktracker.io.TiffFile`
        """

        tf = TiffFile(self.image_path, multifile=multifile)
        return tf

    def get_tif_from_list(self, index=0):
        """Get TiffFile instance from images list.

        Returns
        -------
        tf : :class:`sktracker.io.TiffFile`

        """

        tf = TiffFile(self.image_path_list[index])
        return tf

    def image_iterator(self, position=-2, channel_index=0, z_projection=False, memmap=False):
        """Iterate over image T and Z dimensions. A channel has to be
        choosen and will be excluded from the iterator.

        Notes
        -----
        For now image_iterator load the whole image in memory and build iterator from it.
        To avoid filling memory you can try to use memmap=True but it often fails. In the
        future, image_iterator should only build iterator without filling memory with whole
        image.

        Parameters
        ----------
        position : int
            Dimensions on which you want to iterate. For example, -2 will only
            keep the two last dimensions, usually X and Y.
        channel_index : int or str
            Channel position to remove. If str, Channels metadata will be used.
        memmap : bool
            If True, use `numpy.memmap` to read arrays from file if possible.

        Returns
        -------
        A Python iterator over the image array.
        """

        if not sys.version_info[0] == 2:
            string_types = (str,)
        else:
            string_types = (str, unicode)

        try:
            tf = self.get_tif(multifile=True)
            arr = tf.asarray(memmap=memmap)
        except ValueError:
            log.warning("Failed to open TiffFile with multifile option. Use fallback method.")
            tf = self.get_tif(multifile=False)
            arr = tf.asarray(memmap=memmap).reshape(self.metadata['Shape'])

        if isinstance(channel_index, string_types):
            if 'Channels' in self.metadata.keys():
                channel_index = self.metadata['Channels'].index(channel_index)
            else:
                raise TypeError("'Channels' key is missing in metadata."
                                "Can't find '{}' index".format(channel_index))

        current_dimension_order = list(self.metadata['DimensionOrder'])

        # Get only one single channel
        if 'C' in current_dimension_order:
            channel_position = current_dimension_order.index('C')
            arr = np.take(arr, channel_index, axis=channel_position)
            current_dimension_order.remove('C')

        if z_projection:
            if 'Z' in current_dimension_order:
                z_position = current_dimension_order.index('Z')
                arr = arr.max(axis=z_position)
                current_dimension_order.remove('Z')
            else:
                log.warning("No Z detected. Can't perform Z projection")

        # Define data iterator
        def it():
            for idx in np.ndindex(arr.shape[:position]):
                yield arr[idx]

        return it

    def list_iterator(self, memmap=True):
        """Returns an iterator over each image from
        `self.image_path_list` as an array

        Parameters
        ----------
        memmap : bool
            If True, use `numpy.memmap` to read arrays from file if possible.

        Returns
        -------
        A Python iterator over the image list.
        """
        image_list = self.image_path_list

        def stack_iter():
            for filename in image_list:
                stack = TiffFile(filename).asarray(memmap=memmap)
                yield stack
        return stack_iter
