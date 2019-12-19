# -*- coding: utf-8 -*-

"""
Data Property
=============

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.widgets import (
    DualComboBox, QW_QLineEdit, get_box_value, get_modified_box_signal,
    set_box_value)

# All declaration
__all__ = ['Data2DProp']


# %% CLASS DEFINITIONS
# Define 'Data2D' plot property
class Data2DProp(BasePlotProp):
    # Class attributes
    NAME = "Data2D"
    DISPLAY_NAME = "Data"
    REQUIREMENTS = ['data_table_plugin', 'draw_plot', 'labelChanged']
    WIDGET_NAMES = ['data_label_box', 'x_data_box', 'y_data_box']

    # This function creates and returns the data label box
    def data_label_box(self):
        # Make a lineedit for setting the label of the plot
        data_label_box = QW_QLineEdit()
        data_label_box.setToolTip("Label of this plot")
        get_modified_box_signal(data_label_box).connect(self.labelChanged)

        # Return name and box
        return('Label', data_label_box)

    # This function creates and returns the x-axis data box
    def x_data_box(self):
        # Make a combobox for setting the x-axis data
        x_data_box = DataColumnBox(self.data_table_plugin)
        x_data_box.setToolTip("Data table and column to use for the X-axis "
                              "data")
        get_modified_box_signal(x_data_box).connect(self.draw_plot)

        # Return name and box
        return('X-axis', x_data_box)

    # This function creates and returns the y-axis data box
    def y_data_box(self):
        # Make a combobox for setting the y-axis data
        y_data_box = DataColumnBox(self.data_table_plugin)
        y_data_box.setToolTip("Data table and column to use for the Y-axis "
                              "data")
        get_modified_box_signal(y_data_box).connect(self.draw_plot)

        # Return name and box
        return('Y-axis', y_data_box)


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
        self.set_box_value((-1, -1))

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
