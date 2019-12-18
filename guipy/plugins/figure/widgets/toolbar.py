# -*- coding: utf-8 -*-

"""
Figure Toolbar
==============

"""


# %% IMPORTS
# Built-in imports
from qtpy import QtCore as QC, QtWidgets as QW

# Package imports
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

# GuiPy imports
from guipy.plugins.figure.widgets.options import FigureOptionsDialog
from guipy.widgets import (
    QW_QPushButton, get_box_value, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigureToolbar']


# %% CLASS DEFINITIONS
# Custom FigureToolbar class
class FigureToolbar(NavigationToolbar2QT):
    # Initialize FigureToolbar class
    def __init__(self, data_table_plugin_obj, canvas, parent=None):
        # Save provided data table plugin object
        self.data_table_plugin = data_table_plugin_obj

        # Call super constructor
        super().__init__(canvas, parent, coordinates=False)

        # Set up figure toolbar
        self.init()

    # This function sets up the figure toolbar
    def init(self):
        # Create pointer in figure manager to this toolbar
        self.canvas.manager.toolbar = self

        # Initialize options dialog
        self.options_dialog = FigureOptionsDialog(self)
        self.labels = ['>>> Figure &options...', '<<< Figure &options...']

        # Obtain the first action in the toolbar
        action_0 = self.actions()[0]

        # Create button for showing/hiding extra options
        dialog_but = QW_QPushButton()
        set_box_value(dialog_but, self.labels[self.options_dialog.isHidden()])
        dialog_but.setToolTip("Toggle the figure options menu")
        get_modified_box_signal(dialog_but).connect(self.toggle_options_dialog)
        dialog_but.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        self.insertWidget(action_0, dialog_but)
        self.dialog_but = dialog_but

        # Create button for refreshing the figure
        refresh_but = QW_QPushButton("Refresh")
        refresh_but.setShortcut(QC.Qt.Key_F5)
        get_modified_box_signal(refresh_but).connect(
            self.options_dialog.refresh_figure)
        refresh_but.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        self.insertWidget(action_0, refresh_but)

        # Insert separator
        self.insertSeparator(action_0)

    # This function toggles the options dialog
    @QC.Slot()
    def toggle_options_dialog(self):
        # Toggle the options dialog
        self.options_dialog.setVisible(self.options_dialog.isHidden())
        set_box_value(self.dialog_but,
                      self.labels[self.options_dialog.isHidden()])

        # Refresh the figure if the dialog was closed
        if self.options_dialog.isHidden():
            self.options_dialog.refresh_figure()
