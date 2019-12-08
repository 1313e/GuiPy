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
from guipy.layouts import QW_QGridLayout, QW_QHBoxLayout, QW_QVBoxLayout
from guipy.widgets import (
    QW_QDialog, QW_QComboBox, QW_QLabel, QW_QPushButton, QW_QWidget)

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
        # Set size policies for this options widget
        self.setSizePolicy(QW.QSizePolicy.Ignored, QW.QSizePolicy.Fixed)

        # Initialize options dialog
        self.options_dialog = FigureOptionsDialog(self)
        self.labels = ['>>> Figure options...', '<<< Figure options...']

        # Create main layout
        layout = QW_QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create button for showing/hiding extra options
        dialog_but = QW_QPushButton()
        dialog_but.setText(self.labels[self.options_dialog.isHidden()])
        dialog_but.clicked.connect(self.toggle_options_dialog)
        dialog_but.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        layout.addWidget(dialog_but)
        self.dialog_but = dialog_but

        # Create combobox with available data tables
        tables_box = QW_QComboBox()
        tables_box.addItems(self.tab_widget.tabNames())
        table_label = QW_QLabel("Data table: ")
        table_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        self.tables_box = tables_box
        layout.addWidget(table_label)
        layout.addWidget(tables_box)

        # Connect signals for combobox
        self.tab_widget.tabNameChanged.connect(tables_box.setItemText)
        self.tab_widget.tabWasInserted[int, str].connect(tables_box.insertItem)
        self.tab_widget.tabWasRemoved.connect(tables_box.removeItem)

        # Create combobox with available plot types
        types_box = QW_QComboBox()
        plot_label = QW_QLabel("Plot type: ")
        plot_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        self.types_box = types_box
        layout.addWidget(plot_label)
        layout.addWidget(types_box)

    # This function toggles the options dialog
    @QC.Slot()
    def toggle_options_dialog(self):
        # Toggle the options dialog
        self.options_dialog.setVisible(self.options_dialog.isHidden())
        self.dialog_but.setText(self.labels[self.options_dialog.isHidden()])

        # Toggle the comboboxes
        self.tables_box.setEnabled(self.options_dialog.isHidden())
        self.types_box.setEnabled(self.options_dialog.isHidden())


# Define class for the Figure options dialog
class FigureOptionsDialog(QW_QDialog):
    # Initialize FigureOptionsDialog
    def __init__(self, figure_options_obj, *args, **kwargs):
        # Save provided FigureOptions object
        self.figure_options = figure_options_obj

        # Call super constructor
        super().__init__(figure_options_obj)

        # Set up the figure options dialog
        self.init(*args, **kwargs)

    # This function sets up the figure options dialog
    def init(self):
        # Set dialog properties
        self.setWindowFlags(
            QC.Qt.Dialog |
            QC.Qt.FramelessWindowHint |
            QC.Qt.NoDropShadowWindowHint)

        # Create a layout
        layout = QW_QVBoxLayout()
        self.setLayout(layout)

        # Add a grid layout to it
        grid_layout = QW_QGridLayout()
        layout.addLayout(grid_layout)

        # Add a dummy widgets to the grid layout for testing
        grid_layout.addWidget(QW_QLabel("Test"), 0, 0)
        grid_layout.addWidget(QW_QComboBox(), 1, 0)

        # Add stretch
        layout.addStretch()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        layout.addWidget(button_box)
        close_but = button_box.addButton(button_box.Close)
        close_but.clicked.connect(self.figure_options.toggle_options_dialog)

    # Override showEvent to show the dialog in the proper location
    def showEvent(self, event):
        # Call super event
        super().showEvent(event)

        # Determine the position of the bottom left corner of the figure dock
        dock_pos = self.figure_options.rect().bottomLeft()

        # Determine the size of this dialog
        size = self.size()
        size = QC.QPoint(size.width(), size.height())

        # Determine position of top left corner
        dialog_pos = self.figure_options.mapToGlobal(dock_pos-size)

        # Move it slightly to give some spacing
        dialog_pos.setX(dialog_pos.x()-12)

        # Move the dialog there
        self.move(dialog_pos)
