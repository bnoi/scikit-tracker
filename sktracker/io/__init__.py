"""`sktracker.io` module is designed to easly and quickly open Tiff files and
to be able to parse and import any kind of metadata.

Finally, an OME module is provided to read and write OME xml metadata. See
https://www.openmicroscopy.org/site/support/ome-model/ for details.

"""

from .tifffile import imsave
from .tifffile import imread
from .tifffile import imshow
from .tifffile import TiffFile
from .tifffile import TiffSequence

__all__ = ['imsave', 'imread', 'imshow', 'TiffFile', 'TiffSequence']
