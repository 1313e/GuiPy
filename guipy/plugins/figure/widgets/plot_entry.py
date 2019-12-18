# -*- coding: utf-8 -*-

"""
Figure Plot Entry
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from matplotlib import rcParams
from matplotlib.lines import lineMarkers, lineStyles
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.widgets import (
    BaseBox, ColorBox, DualComboBox, QW_QComboBox, QW_QDoubleSpinBox,
    QW_QGroupBox, QW_QLineEdit, QW_QWidget, get_box_value,
    get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigurePlotEntry']


# %% CLASS DEFINITIONS
# Create custom class for make a plot entry
class FigurePlotEntry(BaseBox):
    # Signals
    labelChanged = QC.Signal(str)

    # Initialize PlotEntryBox class
    def __init__(self, name, figure_options_obj, parent=None, *args, **kwargs):
        # Save provided FigureOptions object
        self.figure_options = figure_options_obj
        self.data_table_plugin = figure_options_obj.data_table_plugin
        self.figure = figure_options_obj.figure
        self.axis = self.figure.gca()

        # Call super constructor
        super().__init__(parent)

        # Set up the plot entry box
        self.init(name, *args, **kwargs)

    # This function sets up the plot entry box
    def init(self, name):
        # Create layout for this plot entry box
        layout = QW_QFormLayout(self)

        # DATA
        # Create a group box for setting the data of the plot
        data_group = QW_QGroupBox("Data")
        layout.addRow(data_group)
        data_layout = QW_QFormLayout(data_group)

        # Make a lineedit for setting the label of the plot
        data_label_box = QW_QLineEdit()
        get_modified_box_signal(data_label_box).connect(self.labelChanged)
        data_layout.addRow("Label", data_label_box)
        self.data_label_box = data_label_box

        # Make a combobox for setting the x-axis data
        x_data_box = DataColumnBox(self.data_table_plugin)
        set_box_value(x_data_box, (-1, -1))
        get_modified_box_signal(x_data_box).connect(self.draw_line)
        data_layout.addRow("X-axis", x_data_box)
        self.x_data_box = x_data_box

        # Make a combobox for setting the y-axis data
        y_data_box = DataColumnBox(self.data_table_plugin)
        set_box_value(y_data_box, (-1, -1))
        get_modified_box_signal(y_data_box).connect(self.draw_line)
        data_layout.addRow("Y-axis", y_data_box)
        self.y_data_box = y_data_box

        # LINE
        # Create a group box for setting the line properties of the plot
        line_group = QW_QGroupBox("Line")
        layout.addRow(line_group)
        line_layout = QW_QFormLayout(line_group)

        # Make a combobox for setting the line style
        line_style_box = self.create_linestyle_box()
        get_modified_box_signal(line_style_box).connect(self.update_line)
        line_layout.addRow("Style", line_style_box)
        self.line_style_box = line_style_box

        # Make a spinbox for setting the line width
        line_width_box = self.create_linewidth_box()
        get_modified_box_signal(line_width_box).connect(self.update_line)
        line_layout.addRow("Width", line_width_box)
        self.line_width_box = line_width_box

        # Make a colorbox for setting the line color
        line_color_box = ColorBox()
        get_modified_box_signal(line_color_box).connect(self.update_line)
        line_layout.addRow("Color", line_color_box)
        self.line_color_box = line_color_box

        # MARKER
        # Create a group box for setting the marker properties of the plot
        marker_group = QW_QGroupBox("Marker")
        layout.addRow(marker_group)
        marker_layout = QW_QFormLayout(marker_group)

        # Make a combobox for setting the marker style
        marker_style_box = self.create_markerstyle_box()
        get_modified_box_signal(marker_style_box).connect(self.update_line)
        marker_layout.addRow("Style", marker_style_box)
        self.marker_style_box = marker_style_box

        # Make a spinbox for setting the marker size
        marker_size_box = self.create_markersize_box()
        get_modified_box_signal(marker_size_box).connect(self.update_line)
        marker_layout.addRow("Size", marker_size_box)
        self.marker_size_box = marker_size_box

        # Make a colorbox for setting the marker color
        marker_color_box = ColorBox()
        get_modified_box_signal(marker_color_box).connect(self.update_line)
        marker_layout.addRow("Color", marker_color_box)
        self.marker_color_box = marker_color_box

        # Connect signals
        self.labelChanged.connect(self.set_line_label)

        # Save that currently no line exists and draw the start line
        self.line = None
        set_box_value(data_label_box, name)
        self.draw_line()

    # Override closeEvent to remove the plot from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Remove the plot from the figure if it exists
        if self.line in self.axis.lines:
            self.axis.lines.remove(self.line)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function draws the 2D line plot
    @QC.Slot()
    def draw_line(self):
        # Obtain the x and y columns
        try:
            xcol = get_box_value(self.x_data_box)[1]
            ycol = get_box_value(self.y_data_box)[1]
        # If any of the columns cannot be called, return
        except IndexError:
            return

        # If either xcol or ycol is None, return
        if xcol is None or ycol is None:
            return

        # If xcol and ycol are not the same shape, return
        if(len(xcol) != len(ycol)):
            return

        # If the current saved line is not already in the figure, make one
        if self.line not in self.axis.lines:
            self.line = self.axis.plot(xcol, ycol)[0]
            self.set_line_label()
            self.update_line()
        else:
            self.line.set_xdata(xcol)
            self.line.set_ydata(ycol)

    # This function updates the 2D line plot
    @QC.Slot()
    def update_line(self):
        # If line currently exists, update it
        if self.line is not None:
            # Update line style, width and color
            self.line.set_linestyle(get_box_value(self.line_style_box))
            self.line.set_linewidth(get_box_value(self.line_width_box))
            self.line.set_color(get_box_value(self.line_color_box))

            # Update marker style, size and color
            self.line.set_marker(get_box_value(self.marker_style_box))
            self.line.set_markersize(get_box_value(self.marker_size_box))
            self.line.set_markeredgecolor(get_box_value(self.marker_color_box))
            self.line.set_markerfacecolor(get_box_value(self.marker_color_box))

    # This function sets the label of a line
    @QC.Slot()
    def set_line_label(self):
        # If line currently exists, set its label
        if self.line is not None:
            self.line.set_label(get_box_value(self.data_label_box))

    # This function creates a linestyle box
    def create_linestyle_box(self):
        # Obtain list with all supported linestyles
        linestyles_lst = [(key, value[6:]) for key, value in lineStyles.items()
                          if value != '_draw_nothing']
        linestyles_lst.append(('', 'nothing'))
        linestyles_lst.sort(key=lambda x: x[0])

        # Make combobox for linestyles
        linestyle_box = QW_QComboBox()
        for i, (linestyle, tooltip) in enumerate(linestyles_lst):
            linestyle_box.addItem(linestyle)
            linestyle_box.setItemData(i, tooltip, QC.Qt.ToolTipRole)
        set_box_value(linestyle_box, rcParams['lines.linestyle'])
        linestyle_box.setToolTip("Linestyle to be used for this plot")
        return(linestyle_box)

    # This function creates a linewidth box
    def create_linewidth_box(self):
        # Make a double spinbox for linewidth
        linewidth_box = QW_QDoubleSpinBox()
        linewidth_box.setRange(0, 9999999)
        linewidth_box.setSuffix(" pts")
        set_box_value(linewidth_box, rcParams['lines.linewidth'])
        linewidth_box.setToolTip("Width of the plotted line")
        return(linewidth_box)

    # This function creates a marker box
    def create_markerstyle_box(self):
        # Obtain list with all supported markers
        markers_lst = [(key, value) for key, value in lineMarkers.items()
                       if(value != 'nothing' and isinstance(key, str))]
        markers_lst.append(('', 'nothing'))
        markers_lst.sort(key=lambda x: x[0])

        # Make combobox for markers
        marker_box = QW_QComboBox()
        for i, (marker, tooltip) in enumerate(markers_lst):
            marker_box.addItem(marker)
            marker_box.setItemData(i, tooltip, QC.Qt.ToolTipRole)
        set_box_value(marker_box, rcParams['lines.marker'])
        marker_box.setToolTip("Marker to be used for this plot")
        return(marker_box)

    # This function creates a markersize box
    def create_markersize_box(self):
        # Make a double spinbox for markersize
        markersize_box = QW_QDoubleSpinBox()
        markersize_box.setRange(0, 9999999)
        markersize_box.setSuffix(" pts")
        markersize_box.setToolTip("Size of the plotted markers")
        set_box_value(markersize_box, rcParams['lines.markersize'])
        return(markersize_box)


# Create custom class for setting the data column used in plots
class DataColumnBox(DualComboBox):
    # Initialize DataColumnBox class
    def __init__(self, data_table_plugin_obj, parent=None, *args, **kwargs):
        # Save provided data_table_obj
        self.data_table_plugin = data_table_plugin_obj
        self.tab_widget = data_table_plugin_obj.tab_widget

        # Call super constructor
        super().__init__((False, False), r"<html>&rarr;</html>", parent, *args,
                         **kwargs)

    # This function sets up the data column box
    def init(self, *args, **kwargs):
        # Call super setup
        super().init(*args, **kwargs)

        # Extract the two created comboboxes
        tables_box, columns_box = self[:]
        self.tables_box = tables_box
        self.columns_box = columns_box

        # Add items to data tables combobox
        for i, name in enumerate(self.tab_widget.tabNames()):
            tables_box.addItem(name)
            self.set_tables_box_item_tooltip(i, name)

        # Connect signals for tables_box
        self.tab_widget.tabNameChanged.connect(tables_box.setItemText)
        self.tab_widget.tabNameChanged.connect(
            self.set_tables_box_item_tooltip)
        self.tab_widget.tabWasInserted[int, str].connect(tables_box.insertItem)
        self.tab_widget.tabWasInserted[int, str].connect(
            self.set_tables_box_item_tooltip)
        self.tab_widget.tabWasRemoved.connect(tables_box.removeItem)
        get_modified_box_signal(tables_box, int).connect(
            self.set_columns_box_table)

        # Set initial contents of columns_box
        self.data_table = None
        self.model = None
        self.set_columns_box_table(get_box_value(tables_box, int))

    # This function sets the tooltip of an item in the tables box
    @QC.Slot(int, str)
    def set_tables_box_item_tooltip(self, index, text):
        self.tables_box.setItemData(index, text, QC.Qt.ToolTipRole)

    # This function sets the data table in the columns box
    @QC.Slot(int)
    def set_columns_box_table(self, index):
        # Clear the columns_box of all its items
        self.columns_box.clear()

        # If the currently saved data table still exists, disconnect signals
        if(self.data_table_plugin.tab_widget.indexOf(self.data_table) != -1):
            self.model.columnsInserted.disconnect(self.insert_columns)
            self.model.columnsRemoved.disconnect(self.remove_columns)
            self.model.columnDisplayNameChanged.disconnect(
                self.columns_box.setItemText)
            self.model.columnDisplayNameChanged.disconnect(
                self.set_columns_box_item_tooltip)

        # If currently a data table is selected, obtain its columns
        if(index != -1):
            # Obtain the data table associated with the provided index
            self.data_table = self.data_table_plugin.dataTable(index)
            self.model = self.data_table.model

            # Add all columns in this data table to the columns box
            for i, name in enumerate(self.model.columnDisplayNames()):
                self.columns_box.addItem(name)
                self.set_columns_box_item_tooltip(i, name)

            # Connect signals for columns_box
            self.model.columnsInserted.connect(self.insert_columns)
            self.model.columnsRemoved.connect(self.remove_columns)
            self.model.columnDisplayNameChanged.connect(
                self.columns_box.setItemText)
            self.model.columnDisplayNameChanged.connect(
                self.set_columns_box_item_tooltip)

        # Else, set data_table and model to None
        else:
            self.data_table = None
            self.model = None

    # This function sets the tooltip of an item in the columns box
    @QC.Slot(int, str)
    def set_columns_box_item_tooltip(self, index, text):
        self.columns_box.setItemData(index, text, QC.Qt.ToolTipRole)

    # This function inserts column display names into the columns box
    @QC.Slot(QC.QModelIndex, int, int)
    def insert_columns(self, parent, first, last):
        # Insert all columns between first and last+1 to the columns box
        for i in range(first, last+1):
            display_name = self.model.dataColumn(i).display_name
            self.columns_box.insertItem(i, display_name)
            self.set_columns_box_item_tooltip(i, display_name)

    # This function removes column display names from the columns box
    @QC.Slot(QC.QModelIndex, int, int)
    def remove_columns(self, parent, first, last):
        # If the currently set column has been removed, set it to -1
        if get_box_value(self.columns_box, int) in range(first, last+1):
            set_box_value(self.columns_box, -1)

        # Remove all columns between first and last+1 from the columns box
        for i in reversed(range(first, last+1)):
            self.columns_box.removeItem(i)

    # This function retrieves the data table and column currently selected
    def get_box_value(self, *args, **kwargs):
        """
        Returns the currently selected data table and its associated column.

        Returns
        -------
        data_table : :obj:`~guipy.plugins.data_table.widgets.DataTableWidget` \
            object
            The data table that is currently set in this data column box.
        data_column : :obj:`~guipy.plugins.data_table.widgets.DataTableColumn`\
            object
            The data table column in `data_table` that is currently set.

        """

        # Obtain the currently selected column
        column_index = get_box_value(self.columns_box, int)

        # If currently a valid column is selected, return table and column
        if(column_index != -1):
            return(self.data_table, self.model.dataColumn(column_index))
        # Else, return (None, None)
        else:
            return(None, None)
