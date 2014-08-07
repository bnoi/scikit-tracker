# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import warnings
import logging
log = logging.getLogger(__name__)

__all__ = ['load_matplotlib']


def load_matplotlib(preferreds=["Qt4Agg"]):
    """Try to load matplotlib.
    """

    try:
        import matplotlib
    except ImportError:
        log.info("Matplotlib not installed.")
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        backend = _load_backends(preferreds)

        if not backend:
            backend = _load_backends(matplotlib.rcsetup.all_backends)

    if backend:
        log.info("Matplotlib backend '{}' has been loaded.".format(backend))
    else:
        log.info("No matplotlib backends loaded")

    return backend


def _load_backends(backends):
    """Try to load a list of backends.
    """
    import matplotlib

    success = False
    i = 0
    while not success and i < len(backends):
        backend = backends[i]
        i += 1
        try:
            matplotlib.use(backend, force=True)
            import matplotlib.pyplot as plt
            success = True
        except ImportError:
            pass

    if success:
        return backend
    else:
        return None
