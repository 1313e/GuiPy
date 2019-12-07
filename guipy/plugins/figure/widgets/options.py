# -*- coding: utf-8 -*-

"""
Figure Options
==============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QGridLayout, QW_QVBoxLayout
from guipy.widgets import QW_QComboBox, QW_QLabel, QW_QWidget

# All declaration
__all__ = ['FigureOptions']


# %% CLASS DEFINITIONS
# Define class for the Figure options widget
class FigureOptions(QW_QWidget):
    # Initialize FigureOptions
    def __init__(self, data_table_obj, parent=None, *args, **kwargs):
        # Save provided data table object
        self.data_table = data_table_obj
        self.tab_widget = self.data_table.tab_widget

        # Call super constructor
        super().__init__(parent)

        # Set up the figure options
        self.init(*args, **kwargs)

    # This function sets up the figure options
    def init(self):
        # Set show/hide labels
        self.show_labels = ['Hide Options...', 'Show Options...']

        # Set the options to be hidden
#        self.setHidden(True)

        # Create a layout
        layout = QW_QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Add a separator to the layout
        layout.addSeparator(row=0)

        # Create combobox with available data tables
        tables_box = QW_QComboBox()
        tables_box.addItems(self.tab_widget.tabNames())
        layout.addWidget(QW_QLabel("Data table: "), 1, 0)
        layout.addWidget(tables_box, 1, 1)

        # Connect signals for combobox
        self.tab_widget.tabNameChanged.connect(tables_box.setItemText)
        self.tab_widget.tabWasInserted[int, str].connect(tables_box.insertItem)
        self.tab_widget.tabWasRemoved.connect(tables_box.removeItem)

        # Create combobox with available plot types
        types_box = QW_QComboBox()
        layout.addWidget(QW_QLabel("Plot type: "), 2, 0)
        layout.addWidget(types_box, 2, 1)

        # Add a layout to fill the rest of the grid
        filler_layout = QW_QVBoxLayout()
        filler_layout.addStretch()
        layout.addLayout(filler_layout, layout.rowCount(), 0, -1, -1)
