# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(FigureCanvas):

    def __init__(self, figure, parent):
        """
        """
        super(MatplotlibWidget, self).__init__(figure)
        self.setParent(parent)

        self.fig = figure

    def close_figure(self):
        """
        """
        if self.fig:
            self.fig.clf()
            plt.close(self.fig)
            self.fig = None
