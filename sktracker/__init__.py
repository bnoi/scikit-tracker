"""Object detection and tracking for cell biology

`scikit-learn` is bla bla bla.

Subpackages
-----------
color
    Color space conversion.

"""

try:
    from .version import __version__
except ImportError: # pragma: no cover
    __version__ = "dev" # pragma: no cover

from . import utils
