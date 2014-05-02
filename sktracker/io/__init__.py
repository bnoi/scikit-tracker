
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


""":mod:`sktracker.io` module is designed to easly and quickly open Tiff files and
to be able to parse and import any kind of metadata.

Finally, an OME module is provided to read and write OME xml metadata. See
https://www.openmicroscopy.org/site/support/ome-model/ for details.
"""

from .tifffile import imsave
from .tifffile import imread
from .tifffile import imshow
from .tifffile import TiffFile
from .tifffile import TiffSequence

from .ome import OMEModel
from .stackio import StackIO
from .metadataio import get_metadata
from .metadataio import validate_metadata
from .objectsio import ObjectsIO


__all__ = ['get_metadata', 'OMEModel', 'imsave', 'imread', 'imshow',
           'TiffFile', 'TiffSequence', 'StackIO', 'validate_metadata',
           'ObjectsIO']
