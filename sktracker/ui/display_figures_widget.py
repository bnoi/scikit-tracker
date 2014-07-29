# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import sys

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from . import MatplotlibWidget


def display_figures(figure_generator):
    """Display several Matplotlib figures with "next" and "previous" buttons.

    Parameters
    ----------
    figure_generator : tuple (python generator, string)
        Should return :class:`matplotlib.figure.Figure` object and a title.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>>
    >>> def fig_generator():
    >>>     plt.ioff()
    >>>     for i in range(1, 11):
    >>>         x = np.linspace(-10, 10, 100)
    >>>         y = np.sin(x * i)
    >>>         fig = plt.figure()
    >>>         ax = fig.add_subplot(111)
    >>>         ax.plot(x, y)
    >>>         plt.close(fig)
    >>>         yield fig, str(i)
    >>>
    >>> display_figures(fig_generator())
    """

    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(sys.argv)

    app.aboutToQuit.connect(app.deleteLater)

    fig_w = DisplayFiguresWidget()
    fig_w.add_figures(figure_generator)
    fig_w.show()

    status = app.exec_()
    sys.exit(status)


class DisplayFiguresWidget(QtGui.QWidget):

    def __init__(self):
        """
        """
        super(DisplayFiguresWidget, self).__init__()

        self.init_ui()
        self.m_widget = None

    def init_ui(self):
        """
        """
        self.setWindowTitle('Test')
        self.setLayout(QtGui.QVBoxLayout())

        self.layout_buttons = QtGui.QHBoxLayout()
        self.layout().addLayout(self.layout_buttons)

        self.layout_buttons.addStretch(1)

        self.status = QtGui.QLabel(self)
        self.layout_buttons.addWidget(self.status)

        self.previous_figure_button = QtGui.QPushButton("Previous")
        self.layout_buttons.addWidget(self.previous_figure_button)

        self.next_figure_button = QtGui.QPushButton("Next")
        self.layout_buttons.addWidget(self.next_figure_button)

        self.next_figure_button.clicked.connect(self.next_figure)
        self.previous_figure_button.clicked.connect(self.previous_figure)

        self.plot_canvas = None
        self.nav_toolbar = None
        self.fig_generator = None
        self.current_fig = None
        self.figures_list = []
        self.i = -1

    def add_figures(self, fig_generator):
        """
        """
        self.fig_generator = fig_generator
        self.next_figure()

    def add_figure(self, args):
        """
        """
        figure, title = args

        mess = "{} | Figure n°{}"
        self.status.setText(mess.format(title, self.i))

        self.current_fig = figure
        if figure not in self.figures_list:
            self.figures_list.append(args)
        self.remove_figure()

        self.plot_canvas = MatplotlibWidget(figure, self)
        self.nav_toolbar = NavigationToolbar(self.plot_canvas, self)

        self.layout().insertWidget(0, self.nav_toolbar)
        self.layout().insertWidget(1, self.plot_canvas)

    def remove_figure(self):
        """
        """
        if self.plot_canvas:
            self.layout().removeWidget(self.plot_canvas)
            self.plot_canvas.deleteLater()
            self.plot_canvas = None
        if self.nav_toolbar:
            self.layout().removeWidget(self.nav_toolbar)
            self.nav_toolbar.deleteLater()
            self.nav_toolbar = None

    def next_figure(self):
        """
        """
        if self.i == -1 or self.current_fig == self.figures_list[-1][0]:
            self.i += 1

            try:
                fig, title = self.fig_generator.__next__()
                self.add_figure((fig, title))
            except StopIteration:
                self.status.setText("No next figure")
        else:
            self.i += 1
            self.add_figure(self.figures_list[self.i])

    def previous_figure(self):
        """
        """
        if self.i > 0:
            self.i -= 1
            self.add_figure(self.figures_list[self.i])
        else:
            self.status.setText("No previous figure")
