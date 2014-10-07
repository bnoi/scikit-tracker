# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
log = logging.getLogger(__name__)

import pyqtgraph as pg
import numpy as np

from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtCore
from pyqtgraph import dockarea
import pyqtgraph.exporters as pgexporters

from .viewbox import DataSelectorViewBox


class TrajectoriesWidget(QtGui.QWidget):
    """Display a Trajectories object. Trajectories can be modified manually inside the widget:
        - remove spots
        - cut / merge /remove / duplicate trajectory(ies)

    Parameters
    ----------
    trajs : :class:`sktracker.trajectories.Trajectories` or list
        Trajectories or list of Trajectories to show in the widget.
    names : str or list
        Name(s) of the Trajectories (optional).
    xaxis : str
        Trajectories columns to display on x axis (can be changed in the widget).
    yaxis : str
        Trajectories columns to display on y axis (can be changed in the widget).
    scale_x : float
        Scale factor to use on x axis.
    scale_y :
        Scale factor to use on y axis.
    save_hook : function
        If not None a "Save" button will appear and this function will be called once the button
        is clicked/enabled.
    parent : :class:`QtGui.QWidget`
        Qt parent.

    Examples
    --------
    >>> from sktracker.ui import TrajectoriesWidget
    >>> from sktracker import data
    >>> from sktracker.trajectories import Trajectories
    >>> trajs = data.brownian_trajs_df()
    >>> trajs = Trajectories(trajs)
    >>> # Relabel to true label
    >>> trajs.relabel(trajs.true_label)
    >>> tw = TrajectoriesWidget(trajs, names="My traj",
                                xaxis='t', yaxis='x',
                                scale_x=1, scale_y=1,
                                save_hook=None)
    >>> tw.show()

    """

    sig_traj_change = QtCore.Signal(int)
    sig_axis_change = QtCore.Signal(str)
    sig_update_trajectories = QtCore.Signal()

    def __init__(self, trajs, names=None,
                 xaxis='t', yaxis='x',
                 scale_x=1, scale_y=1,
                 save_hook=None,
                 parent=None):

        super().__init__(parent=parent)

        self.setWindowTitle("Trajectories plot")

        if parent is None:
            self.resize(1000, 500)

        if isinstance(trajs, list):
            self.all_trajs = trajs
            if names:
                self.names = names
            else:
                self.names = ["Trajectory n°{}".format(i + 1) for i in range(len(self.all_trajs))]
        else:
            self.all_trajs = [trajs]
            if names:
                self.names = [names]
            else:
                self.names = ["Trajectory n°1"]

        self.all_trajs_historic = [[] for _ in self.all_trajs]

        self.trajs = self.all_trajs[0]
        self.name = self.names[0]
        self.len_trajs = len(self.all_trajs)

        if 'label' not in self.trajs.index.names:
            self.trajs.set_level_label()

        self.curve_width = 1
        self.scatter_size = 8

        self.xaxis = xaxis
        self.yaxis = yaxis
        self.scale_x = scale_x
        self.scale_y = scale_y

        self.save_hook = save_hook

        self.setup_ui()
        self.set_trajectories(0)

        self.selection_box.setTitle('')

    # Message management

    def update_mouse_infos(self, pos):
        """
        """
        pos = self.pw.plotItem.vb.mapDeviceToView(pos)

        mess = ""
        mess += "x = {x}\ny = {y}\n"
        # mess += "label = {label}\ntime = {time}\n"
        # mess += "w = {w}\nI = {I}\n"

        x = np.round(pos.x(), 2)
        y = np.round(pos.y(), 2)

        args = dict(x=x, y=y, label=None, time=None, w=None, I=None)
        mess = mess.format(**args)

        self.mouse_text.setText(mess)

    def update_selection_infos(self):
        """
        """

        if not hasattr(self, 'selection_tree'):
            return

        self.selection_tree.clear()

        i = 0
        for item in self.traj_items:
            if item.is_selected and isinstance(item, pg.SpotItem):
                i += 1
                t_stamp, label = item.data()
                title = "{}, {}".format(t_stamp, label)
                twi = QtGui.QTreeWidgetItem([title])

                peak = self.trajs.loc[t_stamp, label]
                for l in self.column_to_display:
                    ctwi = QtGui.QTreeWidgetItem(["{} : {}".format(l, peak[l])])
                    twi.addChild(ctwi)

                self.selection_tree.addTopLevelItem(twi)

        self.selection_box.setTitle('Selected Items ({})'.format(i))

    # UI methods

    def setup_ui(self):
        """
        """

        self.setLayout(QtGui.QVBoxLayout())

        self.area = dockarea.DockArea()
        self.layout().addWidget(self.area)

        self.dock_traj = dockarea.Dock("Trajectories Plot", size=(3, 12))
        self.dock_info = dockarea.Dock("Info Panel", size=(1, 12))
        self.dock_buttons = dockarea.Dock("Buttons", size=(3, 1), hideTitle=True)
        self.dock_status = dockarea.Dock("Status", size=(3, 0.5), hideTitle=True)
        self.area.addDock(self.dock_traj, 'left')
        self.area.addDock(self.dock_info, 'right', self.dock_traj)
        self.area.addDock(self.dock_buttons, 'bottom')
        self.area.addDock(self.dock_status, 'bottom')

        # Trajectory Plot Dock

        self.vb = DataSelectorViewBox()
        self.pw = pg.PlotWidget(viewBox=self.vb)
        self.vb.traj_widget = self
        self.dock_traj.addWidget(self.pw)
        self.dock_traj.layout.setContentsMargins(5, 5, 5, 5)

        self.dock_status.layout.setContentsMargins(5, 5, 5, 5)
        self.status = QtGui.QLabel(self)
        self.dock_status.addWidget(self.status)

        self.pw.scene().sigMouseMoved.connect(self.update_mouse_infos)

        self.setup_buttons()
        self.setup_menus()

    def setup_menus(self):
        """
        """
        self.menu_spots = QtGui.QMenu("Spots")

        # action_add_spot = QtGui.QAction("Add spot", self.menu_spots)
        # self.menu_spots.addAction(action_add_spot)
        # action_add_spot.triggered.connect(lambda x: x)

        action_remove_spot = QtGui.QAction("Remove spots", self.menu_spots)
        self.menu_spots.addAction(action_remove_spot)
        action_remove_spot.setShortcut("Del")
        action_remove_spot.triggered.connect(self.remove_spots)

        self.menu_trajs = QtGui.QMenu("Trajectories")

        action_merge_trajs = QtGui.QAction("Merge two trajectories", self.menu_trajs)
        self.menu_trajs.addAction(action_merge_trajs)
        action_merge_trajs.triggered.connect(self.merge_trajs)

        action_remove_traj = QtGui.QAction("Remove trajectory", self.menu_trajs)
        self.menu_trajs.addAction(action_remove_traj)
        action_remove_traj.triggered.connect(self.remove_traj)

        action_cut_traj = QtGui.QAction("Cut trajectory", self.menu_trajs)
        self.menu_trajs.addAction(action_cut_traj)
        action_cut_traj.triggered.connect(self.cut_traj)

        action_duplicate_traj = QtGui.QAction("Duplicate trajectory", self.menu_trajs)
        self.menu_trajs.addAction(action_duplicate_traj)
        action_duplicate_traj.triggered.connect(self.duplicate_traj)

        self.vb.menu.addSeparator()
        self.vb.menu.addMenu(self.menu_spots)
        self.vb.menu.addMenu(self.menu_trajs)

    def setup_buttons(self):
        """
        """

        # Build buttons Dock

        self.dock_buttons_parent = QtGui.QWidget()
        self.dock_buttons_parent.setLayout(QtGui.QHBoxLayout())
        self.dock_buttons.addWidget(self.dock_buttons_parent)

        # Build axis buttons

        self.axis_container = QtGui.QWidget()
        self.axis_container.setLayout(QtGui.QGridLayout())

        self.cb_xaxis_label = QtGui.QLabel('X axis : ')
        self.axis_container.layout().addWidget(self.cb_xaxis_label, 0, 0)
        self.cb_xaxis = QtGui.QComboBox()
        self.axis_container.layout().addWidget(self.cb_xaxis, 0, 1)

        self.cb_yaxis_label = QtGui.QLabel('Y axis : ')
        self.axis_container.layout().addWidget(self.cb_yaxis_label, 1, 0)
        self.cb_yaxis = QtGui.QComboBox()
        self.axis_container.layout().addWidget(self.cb_yaxis, 1, 1)

        self.setup_axis_buttons_label()

        self.cb_xaxis.currentIndexChanged.connect(self.set_xaxis)
        self.cb_yaxis.currentIndexChanged.connect(self.set_yaxis)

        self.dock_buttons_parent.layout().addWidget(self.axis_container)

        # Build undo / redo buttons

        self.history_container = QtGui.QWidget()
        self.history_container.setLayout(QtGui.QGridLayout())

        self.but_undo = QtGui.QPushButton("Undo < (0)")
        self.history_container.layout().addWidget(self.but_undo, 0, 0)
        self.but_undo.clicked.connect(self.undo)

        self.but_redo = QtGui.QPushButton("Redo > (0)")
        self.history_container.layout().addWidget(self.but_redo, 1, 0)
        self.but_redo.clicked.connect(self.redo)

        self.dock_buttons_parent.layout().addWidget(self.history_container)

        # Build select / unselect buttons

        self.selection_container = QtGui.QWidget()
        self.selection_container.setLayout(QtGui.QGridLayout())

        self.but_select_all = QtGui.QPushButton("Select All")
        self.selection_container.layout().addWidget(self.but_select_all, 0, 0)
        self.but_select_all.clicked.connect(self.select_all_items)

        self.but_unselect_all = QtGui.QPushButton("Unselect All")
        self.selection_container.layout().addWidget(self.but_unselect_all, 1, 0)
        self.but_unselect_all.clicked.connect(self.unselect_all_items)

        self.dock_buttons_parent.layout().addWidget(self.selection_container)

        # Build trajs selector

        if self.len_trajs > 1:
            self.all_trajs_container = QtGui.QWidget()
            self.all_trajs_container.setLayout(QtGui.QGridLayout())

            self.all_trajs_label = QtGui.QLabel()
            self.all_trajs_container.layout().addWidget(self.all_trajs_label, 0, 0)

            self.all_trajs_previous = QtGui.QPushButton("Next >")
            self.all_trajs_container.layout().addWidget(self.all_trajs_previous, 1, 0)
            self.all_trajs_previous.clicked.connect(self.next_traj)

            self.all_trajs_next = QtGui.QPushButton("Previous <")
            self.all_trajs_container.layout().addWidget(self.all_trajs_next, 2, 0)
            self.all_trajs_next.clicked.connect(self.previous_trajs)

            self.dock_buttons_parent.layout().addWidget(self.all_trajs_container)

        # Build save button

        if self.save_hook:
            self.dock_buttons_parent.layout().addStretch(1)
            self.but_save = QtGui.QPushButton("Save")
            self.dock_buttons_parent.layout().addWidget(self.but_save)
            self.but_save.clicked.connect(self.save_hook)

        # Build Quit button

        if not self.parent():
            if not self.save_hook:
                self.dock_buttons_parent.layout().addStretch(1)
            self.but_quit = QtGui.QPushButton("Quit")
            self.dock_buttons_parent.layout().addWidget(self.but_quit)
            self.but_quit.clicked.connect(self.close)

        # Build info Panel Dock
        self.dock_info.layout.setContentsMargins(5, 5, 5, 5)

        self.mouse_text = QtGui.QLabel()
        self.dock_info.addWidget(self.mouse_text)

        self.selection_box = QtGui.QGroupBox('Selected Items (0)')
        self.dock_info.addWidget(self.selection_box)

        self.selection_tree = pg.TreeWidget()
        self.selection_tree.setColumnCount(1)
        self.selection_tree.setHeaderLabels(["t_stamp, label"])
        self.selection_box.setLayout(QtGui.QVBoxLayout())
        self.selection_box.layout().addWidget(self.selection_tree)

    def setup_axis_buttons_label(self):
        """
        """

        self.cb_xaxis.clear()
        for label in self.trajs.columns.tolist():
            self.cb_xaxis.addItem(label)

        self.cb_yaxis.clear()
        for label in self.trajs.columns:
            self.cb_yaxis.addItem(label)

        self.set_xaxis(self.xaxis)
        self.set_yaxis(self.yaxis)

    # Items management

    def update_trajectories(self, draggable_value=None, no_axis_update=False):
        """
        """

        self.remove_items()
        self.label_colors = self.trajs.get_colors()

        self.draggable_line = pg.InfiniteLine(angle=90, movable=True)
        if draggable_value:
            self.draggable_line.setValue(draggable_value)
        self.pw.addItem(self.draggable_line)

        self.trajs.sort_index(inplace=True)
        gp = self.trajs.groupby(level='label')

        for label, peaks in gp:

            color = self.label_colors[label]

            coords = peaks.loc[:, [self.xaxis, self.yaxis]].values
            x = coords[:, 0] * self.scale_x
            y = coords[:, 1] * self.scale_y

            index_list = peaks.index.tolist()

            curve = pg.PlotCurveItem(x=x, y=y,
                                     pen={'color': color, 'width': self.curve_width},
                                     clickable=True)
            curve.label = label
            curve.is_selected = False

            self.pw.addItem(curve)
            curve.sigClicked.connect(self.item_clicked)
            self.traj_items.append(curve)

            points_item = pg.ScatterPlotItem(symbol='o',
                                             pen={'color': (0, 0, 0, 0)},
                                             brush=pg.mkBrush(color=color),
                                             size=self.scatter_size)

            points = [{'x': xx, 'y': yy, 'data': idx} for idx, xx, yy in zip(index_list, x, y)]
            points_item.addPoints(points)

            for point in points_item.points():
                point.is_selected = False
                point.parent = points_item
                self.traj_items.append(point)

            points_item.sigClicked.connect(self.points_clicked)
            self.pw.addItem(points_item)

        self.pw.showGrid(x=True, y=True)
        self.pw.setLabel('bottom', self.xaxis)
        self.pw.setLabel('left', self.yaxis)

        if no_axis_update:
            self.cb_xaxis.setCurrentIndex(self.trajs.columns.tolist().index(self.xaxis))
            self.cb_yaxis.setCurrentIndex(self.trajs.columns.tolist().index(self.yaxis))

        self.update_selection_infos()

        self.sig_update_trajectories.emit()

    def points_clicked(self, plot, points):
        """
        """
        for point in points:
            self.item_clicked(point)

    def item_clicked(self, item):
        """
        """
        self.check_control_key(ignore_items=[item])
        if item.is_selected is False:
            self.select_item(item)
        else:
            self.unselect_item(item)

        self.update_selection_infos()

    def select_item(self, item):
        """
        """
        if item.is_selected is False:
            item.is_selected = True
            if isinstance(item, pg.SpotItem):
                item.setPen(width=2, color='r')
                item.setSize(self.scatter_size * 1.5)
            elif isinstance(item, pg.PlotCurveItem):
                color = self.item_colors(item)
                item.setPen(width=self.curve_width * 2, color=color)
            else:
                log.warning("Item {} not handled".format(item))

    def unselect_item(self, item):
        """
        """
        if item.is_selected:
            item.is_selected = False

            if isinstance(item, pg.SpotItem):
                item.setPen(None)
                item.setSize(self.scatter_size)
            elif isinstance(item, pg.PlotCurveItem):
                color = self.item_colors(item)
                item.setPen(width=self.curve_width, color=color)
            else:
                log.warning("Item {} not handled".format(item))

    def remove_item(self, item):
        """
        """
        self.pw.removeItem(item)
        del item

    def remove_items(self):
        """
        """
        self.traj_items = []
        for item in self.pw.items():
            self.remove_item(item)

    def unselect_all_items(self, event=None, ignore_items=[]):
        """
        """
        for item in self.traj_items:
            if item not in ignore_items:
                self.unselect_item(item)
        self.update_selection_infos()
        self.status.setText("Al items unselected")

    def select_all_items(self):
        """
        """
        for item in self.traj_items:
            self.select_item(item)
        self.update_selection_infos()
        self.status.setText("{} items selected".format(len(self.traj_items)))

    def check_control_key(self, ignore_items=[]):
        """Unselect all previously selected items if CTRL key is not pressed.
        """
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers != QtCore.Qt.ControlModifier:
            self.unselect_all_items(ignore_items=ignore_items)

    def item_colors(self, item):
        """
        """
        label = None
        if isinstance(item, pg.SpotItem):
            label = item.data()[1]
        elif isinstance(item, pg.PlotCurveItem):
            label = item.label
        else:
            log.warning("Item {} not handled".format(item))
            return False
        return self.label_colors[label]

    def get_selected_items(self):
        """
        """
        return list(filter(lambda x: x.is_selected, self.traj_items))

    # Trajectories selector

    def set_trajectories(self, i):
        """
        """

        if i < 0 or i >= self.len_trajs:
            return

        self.current_traj_id = i
        self.column_to_display = self.trajs.columns.tolist()
        self.trajs = self.all_trajs[self.current_traj_id]
        self.name = self.names[self.current_traj_id]

        self.historic_trajs = self.all_trajs_historic[self.current_traj_id]
        self.historic_trajs.append(self.trajs)

        self.traj_items = []

        self.update_historic_buttons()

        if 'label' not in self.trajs.index.names:
            self.trajs.set_level_label()

        self.update_trajectories()
        self.set_all_trajs_label()
        self.status.setText(self.name)

        self.sig_traj_change.emit(self.current_traj_id)

    def next_traj(self):
        """
        """
        self.set_trajectories(self.current_traj_id + 1)

    def previous_trajs(self):
        """
        """
        self.set_trajectories(self.current_traj_id - 1)

    def set_all_trajs_label(self):
        """
        """
        if self.len_trajs > 1:
            m = "Trajs selector : {}/{}"
            self.all_trajs_label.setText(m.format(self.current_traj_id + 1, self.len_trajs))

    # Trajectories modifications

    def remove_spots(self, obj):
        """
        """
        items = self.get_selected_items()

        spots = [item.data() for item in items]

        if len(spots) == 0:
            self.status.setText('No spots selected')
            return

        self.trajs = self.trajs.copy()
        self.trajs.remove_spots(spots, inplace=True)

        self.historic_trajs.append(self.trajs)
        self.update_trajectories()
        self.update_historic_buttons()

        self.status.setText('{} spots have been removed'.format(len(spots)))

    def merge_trajs(self, obj):
        """
        """
        items = self.get_selected_items()

        spots = [item.data() for item in items]
        spots = np.array(spots)
        labels = np.unique(spots[:, 1])

        if len(labels) <= 1:
            self.status.setText("You need to select at least two spots from "
                                "two different labels")
            return

        self.trajs = self.trajs.copy()
        self.trajs.merge_segments(labels, inplace=True)

        self.historic_trajs.append(self.trajs)
        self.update_trajectories()
        self.update_historic_buttons()

    def remove_traj(self, obj):
        """
        """
        items = self.get_selected_items()

        spots = [item.data() for item in items]
        spots = np.array(spots)
        labels = np.unique(spots[:, 1])

        if len(labels) == 0:
            self.status.setText("You need to select at least one spot")
            return

        self.trajs = self.trajs.copy()
        self.trajs.remove_segments(labels, inplace=True)

        self.historic_trajs.append(self.trajs)
        self.update_trajectories()
        self.update_historic_buttons()

    def cut_traj(self, obj):
        """
        """
        items = self.get_selected_items()

        spots = [item.data() for item in items]

        if len(spots) != 1:
            self.status.setText("You need to select only one spot")
            return

        self.trajs = self.trajs.copy()
        self.trajs.cut_segments(spots[0], inplace=True)

        self.historic_trajs.append(self.trajs)
        self.update_trajectories()
        self.update_historic_buttons()

    def duplicate_traj(self, obj):
        """
        """
        items = self.get_selected_items()

        spots = [item.data() for item in items]
        spots = np.array(spots)
        labels = np.unique(spots[:, 1])

        if len(labels) != 1:
            self.status.setText("You need to select spots(s) from only one trajectory")
            return

        self.trajs = self.trajs.duplicate_segments(labels[0])

        self.historic_trajs.append(self.trajs)
        self.update_trajectories()
        self.update_historic_buttons()

    # Historic management

    def undo(self):
        """
        """

        i = self.current_traj_index()
        self.trajs = self.historic_trajs[i - 1]

        self.update_trajectories()
        self.update_historic_buttons()

    def redo(self):
        """
        """
        i = self.current_traj_index()
        self.trajs = self.historic_trajs[i + 1]

        self.update_trajectories()
        self.update_historic_buttons()

    def update_historic_buttons(self):
        """
        """

        i = self.current_traj_index()
        self.but_undo.setText('Undo < ({})'.format(i))
        self.but_redo.setText('Redo > ({})'.format(len(self.historic_trajs) - i - 1))

        if self.historic_trajs[0] is self.trajs:
            self.but_undo.setDisabled(True)
        else:
            self.but_undo.setDisabled(False)

        if self.historic_trajs[-1] is self.trajs:
            self.but_redo.setDisabled(True)
        else:
            self.but_redo.setDisabled(False)

    def current_traj_index(self):
        """
        """

        for i, trajs in enumerate(self.historic_trajs):
            if trajs is self.trajs:
                return i

    # Exporters

    def save(self, fname):
        """
        """
        if fname.endswith('.svg'):
            exporter = pgexporters.SVGExporter(self.pw.plotItem)
        elif fname.endswith('.png'):
            exporter = pgexporters.ImageExporter(self.pw.plotItem)
        elif fname.endswith('.jpg'):
            exporter = pgexporters.ImageExporter(self.pw.plotItem)
        elif fname.endswith('.tif'):
            exporter = pgexporters.ImageExporter(self.pw.plotItem)
        else:
            self.status.setText('Wrong filename extension')
            return False

        exporter.export(fname)
        self.status.setText('View saved at {}'.format(fname))

    # Axes setter

    def set_xaxis(self, ax_name, scale=None):
        """
        """
        if isinstance(ax_name, int):
            ax_name = self.cb_xaxis.itemText(ax_name)

        if ax_name not in list(self.trajs.columns):
            self.status.setText('"{}" is not in Trajectories columns'.format(ax_name))
            return

        if self.trajs[ax_name].dtype.kind not in ['i', 'f']:
            return

        self.xaxis = ax_name
        if scale:
            self.scale_x = scale

        self.update_trajectories(no_axis_update=True)
        self.sig_axis_change.emit('x')

    def set_yaxis(self, ax_name, scale=None):
        """
        """
        if isinstance(ax_name, int):
            ax_name = self.cb_yaxis.itemText(ax_name)

        if ax_name not in self.trajs.columns:
            self.status.setText('"{}" is not in Trajectories columns'.format(ax_name))
            return

        if self.trajs[ax_name].dtype.kind not in ['i', 'f']:
            return

        self.yaxis = ax_name
        if scale:
            self.scale_y = scale

        self.update_trajectories(no_axis_update=True)
        self.sig_axis_change.emit('y')
