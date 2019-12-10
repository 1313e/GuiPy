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
    QW_QDialog, QW_QComboBox, QW_QLabel, QW_QPushButton, QW_QWidget,
    get_box_value, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigureOptions']


# %% CLASS DEFINITIONS
# Define class for the Figure options widget
# TODO: Combine this class with the FigureToolbar
class FigureOptions(QW_QWidget):
    # Initialize FigureOptions
    def __init__(self, data_table_obj, figure, parent=None, *args, **kwargs):
        # Save provided data table object
        self.data_table = data_table_obj
        self.tab_widget = self.data_table.tab_widget
        self.figure = figure

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
        self.labels = ['>>> Figure &options...', '<<< Figure &options...']

        # Create main layout
        layout = QW_QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create button for showing/hiding extra options
        dialog_but = QW_QPushButton()
        set_box_value(dialog_but, self.labels[self.options_dialog.isHidden()])
        get_modified_box_signal(dialog_but).connect(self.toggle_options_dialog)
        dialog_but.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        layout.addWidget(dialog_but)
        self.dialog_but = dialog_but

        # Create combobox with available data tables
        tables_box = QW_QComboBox()
        tables_box.addItems(self.tab_widget.tabNames())
        table_label = QW_QLabel("Data &table: ")
        table_label.setBuddy(tables_box)
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
        types_box.addItems(['2D line'])
        plot_label = QW_QLabel("&Plot type: ")
        plot_label.setBuddy(types_box)
        plot_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        self.types_box = types_box
        layout.addWidget(plot_label)
        layout.addWidget(types_box)

    # This function toggles the options dialog
    @QC.Slot()
    def toggle_options_dialog(self):
        # Toggle the options dialog
        self.options_dialog.setVisible(self.options_dialog.isHidden())
        set_box_value(self.dialog_but,
                      self.labels[self.options_dialog.isHidden()])

        # Toggle the comboboxes
        self.tables_box.setEnabled(self.options_dialog.isHidden())
        self.types_box.setEnabled(self.options_dialog.isHidden())


# Define class for the Figure options dialog
class FigureOptionsDialog(QW_QDialog):
    # Initialize FigureOptionsDialog
    def __init__(self, figure_options_obj, *args, **kwargs):
        # Save provided FigureOptions object
        self.figure_options = figure_options_obj
        self.figure = figure_options_obj.figure

        # Call super constructor
        super().__init__(figure_options_obj)

        # Set up the figure options dialog
        self.init(*args, **kwargs)

    # This function sets up the figure options dialog
    def init(self):
        # Install event filter
        self.installEventFilter(self)

        # Set dialog properties
        self.setWindowFlags(
            QC.Qt.Dialog |
            QC.Qt.FramelessWindowHint |
            QC.Qt.NoDropShadowWindowHint)

        # Create a layout
        layout = QW_QVBoxLayout()
        self.setLayout(layout)

        # Add a grid layout to it
        self.grid_layout = self.create_options_grid(0)
        layout.addLayout(self.grid_layout)

        # Add stretch
        layout.addStretch()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        layout.addWidget(button_box)
        close_but = button_box.addButton(button_box.Close)
        get_modified_box_signal(close_but).connect(
            self.figure_options.toggle_options_dialog)

    # This function creates the options grid for the selected plot type
    def create_options_grid(self, index=None):
        # If index is None, obtain the currently selected data table index
        if index is None:
            index = get_box_value(self.figure_options.tables_box, int)

        # Obtain the data table associated with this index
        data_table = self.figure_options.data_table.dataTable(index)
        self.data_table = data_table

        # Create grid layout
        grid_layout = QW_QGridLayout()

        # NOTE: Heavy testing here
        # Add combobox for selecting the data for the x-axis
        x_data_box = QW_QComboBox()
        x_data_box.addItems(data_table.model.columnDisplayNames())
        get_modified_box_signal(x_data_box).connect(self.draw_line)
        grid_layout.addWidget(QW_QLabel("x-data: "), 0, 0)
        grid_layout.addWidget(x_data_box, 0, 1)
        self.x_data_box = x_data_box

        # Add combobox for selecting the data for the y-axis
        y_data_box = QW_QComboBox()
        y_data_box.addItems(data_table.model.columnDisplayNames())
        get_modified_box_signal(y_data_box).connect(self.draw_line)
        grid_layout.addWidget(QW_QLabel("y-data: "), 1, 0)
        grid_layout.addWidget(y_data_box, 1, 1)
        self.y_data_box = y_data_box

        # Save that currently no line exists
        self.line = None

        # Return grid_layout
        return(grid_layout)

    # This function draws the 2D line plot
    @QC.Slot()
    def draw_line(self):
        # Obtain the x and y columns
        xcol = self.data_table.model.dataColumn(get_box_value(self.x_data_box))
        ycol = self.data_table.model.dataColumn(get_box_value(self.y_data_box))

        # Obtain the axis object of this figure
        axis = self.figure.gca()

        # If the current saved line is not already in the figure, make one
        if self.line not in axis.lines:
            self.line = axis.plot(xcol, ycol)[0]
        else:
            self.line.set_xdata(xcol)
            self.line.set_ydata(ycol)

        # Update the figure
        axis.relim()
        axis.autoscale_view(True, True, True)
        self.figure.canvas.draw()

    # Override showEvent to show the dialog in the proper location
    def showEvent(self, event):
        # Call super event
        super().showEvent(event)

        # Determine the position of the top left corner of the figure dock
        dock_pos = self.figure_options.rect().topLeft()

        # Determine the size of this dialog
        size = self.size()
        size = QC.QPoint(size.width(), 0)

        # Determine position of top left corner
        dialog_pos = self.figure_options.mapToGlobal(dock_pos-size)

        # Move it slightly to give some spacing
        dialog_pos.setX(dialog_pos.x()-12)

        # Move the dialog there
        self.move(dialog_pos)

    # Override eventFilter to filter out clicks, ESC and Enter
    def eventFilter(self, widget, event):
        # Check if the event involves anything for which the popup should close
        if((event.type() == QC.QEvent.KeyPress) and
           event.key() in (QC.Qt.Key_Escape,)):
            # Toggle the options dialog
            self.figure_options.toggle_options_dialog()
            return(True)

        # Else, process events as normal
        else:
            return(super().eventFilter(widget, event))
