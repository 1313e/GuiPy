# -*- coding: utf-8 -*-

"""
Figure Plot Entry
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QHBoxLayout, QW_QFormLayout
from guipy.plugins.figure.widgets.types import PLOT_TYPES
from guipy.widgets import (
    QW_QComboBox, QW_QLineEdit, QW_QToolButton, QW_QWidget,
    get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigurePlotEntry']


# %% CLASS DEFINITIONS
# Create custom class for making a plot entry
# TODO: Allow for individual plots to be toggled (toggled QGroupBox?)
# TODO: Write custom QGroupBox that can have a QComboBox as its title?
class FigurePlotEntry(QW_QWidget):
    # Signals
    entryNameChanged = QC.Signal(str)
    entryRemoveRequested = QC.Signal()

    # Initialize FigurePlotEntry class
    def __init__(self, index, name, toolbar, parent=None, *args, **kwargs):
        # Save provided index, name and FigureToolbar object
        self.index = index
        self.name = name
        self.toolbar = toolbar

        # Call super constructor
        super().__init__(parent)

        # Set up the plot entry box
        self.init(*args, **kwargs)

    # This function sets up the plot entry
    def init(self):
        # Create layout for this plot entry
        self.create_entry_layout()

    # This function creates the entry layout
    def create_entry_layout(self):
        # Create layout
        layout = QW_QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.layout = layout

        # Create a name editor layout
        name_layout = QW_QHBoxLayout()
        layout.addRow('Name', name_layout)

        # Create entry name editor
        name_box = QW_QLineEdit()
        name_box.setToolTip("Name of this plot entry")
        set_box_value(name_box, self.name)
        get_modified_box_signal(name_box).connect(self.entryNameChanged)
        name_layout.addWidget(name_box)
        self.name_box = name_box

        # Add a toolbutton for deleting this plot entry
        del_but = QW_QToolButton()
        del_but.setToolTip("Delete this plot entry")
        get_modified_box_signal(del_but).connect(self.entryRemoveRequested)
        name_layout.addWidget(del_but)

        # If this theme has a 'remove' icon, use it
        if QG.QIcon.hasThemeIcon('remove'):
            del_but.setIcon(QG.QIcon.fromTheme('remove'))
        # Else, use a simple cross
        else:
            del_but.setText('X')

        # Create a combobox for choosing a plot type
        plot_types = QW_QComboBox()
        plot_types.addItems(PLOT_TYPES['2D'])
        plot_types.setToolTip("Select the plot type you wish to use for this "
                              "plot entry")
        set_box_value(plot_types, -1)
        get_modified_box_signal(plot_types).connect(self.set_plot_type)
        layout.addRow('Type', plot_types)
        self.plot_types = plot_types

        # Add a separator
        layout.addSeparator()

        # Create a dummy entry to start off
        self.plot_entry = QW_QWidget()
        layout.addRow(self.plot_entry)

    # This function sets the currently used plot type
    @QC.Slot(str)
    def set_plot_type(self, plot_type):
        # Obtain the index of the current plot entry
        index = self.layout.indexOf(self.plot_entry)

        # Remove this plot entry
        self.layout.removeWidget(self.plot_entry)
        self.plot_entry.close()

        # If the plot_type is empty, create dummy widget
        if not plot_type:
            plot_entry = QW_QWidget()
            entry_name = self.name

        # Else, initialize the requested type
        else:
            # Initialize the proper entry
            plot_type = PLOT_TYPES['2D'][plot_type]
            plot_entry = plot_type(self.toolbar)
            entry_name = "%i_%s" % (self.index, plot_type.prefix())

        # Insert the new plot entry
        self.layout.insertRow(index, plot_entry)

        # Save new plot entry as the current entry
        self.plot_entry = plot_entry

        # Save new entry name
        set_box_value(self.name_box, entry_name)

    # Override closeEvent to remove the plot from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Close the plot_type
        self.plot_entry.close()

        # Call super event
        super().closeEvent(*args, **kwargs)
