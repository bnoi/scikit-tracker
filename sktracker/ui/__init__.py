# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
log = logging.getLogger(__name__)

""":mod:`sktracker.ui` module provides several Qt widgets allowing fast and intuitive
work with images/videos, whatever scikit-tracker data handle:-)
"""

mpl_ok = False
try:
    import matplotlib
    matplotlib.use('Qt4Agg')
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
    mpl_ok = True
except:
    log.warning("Matplotlib (Qt4 backend) is not installed on this system.")
    log.warning("sktracker.ui won't be available.")

qt_ok = False
try:
    import PyQt4
    qt_ok = True
except:
    log.warning("PyQt4 is not installed on this system.")
    log.warning("sktracker.ui won't be available.")


if qt_ok and mpl_ok:
    from .matplotlib_widget import MatplotlibWidget
    from .display_figures_widget import DisplayFiguresWidget
    from .display_figures_widget import display_figures

    __all__ = ["MatplotlibWidget", "display_figures", "DisplayFiguresWidget"]
else:
    __all__ = []
