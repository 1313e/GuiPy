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
from guipy.layouts import (
    QW_QFormLayout, QW_QGridLayout, QW_QHBoxLayout, QW_QVBoxLayout)
from guipy.widgets import (
    BaseBox, ColorBox, DualSpinBox, QW_QComboBox, QW_QDialog,
    QW_QDoubleSpinBox, QW_QGroupBox, QW_QLabel, QW_QLineEdit, QW_QPushButton,
    QW_QTabWidget, QW_QWidget, get_box_value, get_modified_box_signal,
    set_box_value)

# All declaration
__all__ = ['FigureOptions']


# %% CLASS DEFINITIONS
# Define class for the Figure options widget
# TODO: Combine this class with the FigureToolbar
class FigureOptions(QW_QWidget):
    # Initialize FigureOptions
    def __init__(self, data_table_plugin_obj, figure, parent=None, *args,
                 **kwargs):
        # Save provided data table plugin object
        self.data_table_plugin = data_table_plugin_obj
        self.tab_widget = self.data_table_plugin.tab_widget
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

        # Add the options tabs to it
        self.options_tabs = self.create_options_tabs(0)
        layout.addWidget(self.options_tabs)

        # Add stretch
        layout.addStretch()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        layout.addWidget(button_box)
        close_but = button_box.addButton(button_box.Close)
        get_modified_box_signal(close_but).connect(
            self.figure_options.toggle_options_dialog)

    # This function creates the options tabwidget for the selected plot type
    def create_options_tabs(self, index=None):
        # Create a tab widget
        tab_widget = QW_QTabWidget()

        # Add figure tab
        tab_widget.addTab(*self.create_figure_tab())

        # Add plots tab
        tab_widget.addTab(*self.create_plots_tab())

        # Save that currently no line exists and draw the start line
        self.line = None
        self.draw_line()

        # Return layout
        return(tab_widget)

    # This function creates the 'Figure' tab
    def create_figure_tab(self):
        # Create a tab
        tab = QW_QWidget()

        # Create layout
        layout = QW_QFormLayout()
        tab.setLayout(layout)

        # Make line edit for title
        title_box = QW_QLineEdit()
        layout.addRow("Title", title_box)

        # X-AXIS
        # Create a group box for the X-axis
        x_axis_group = QW_QGroupBox("X-axis")
        layout.addRow(x_axis_group)
        x_axis_layout = QW_QFormLayout()
        x_axis_group.setLayout(x_axis_layout)

        # Make a box for setting the label on the x-axis
        x_label_box = QW_QLineEdit()
        x_axis_layout.addRow("Label", x_label_box)

        # Make a box for setting the range on the x-axis
        x_range_box = DualSpinBox((float, float))
        x_min_box, x_max_box = x_range_box[:]
        x_min_box.setRange(-9999999, 9999999)
        x_max_box.setRange(-9999999, 9999999)
        x_axis_layout.addRow("Range", x_range_box)

        # Make a box for setting the scale on the x-axis
        x_scale_box = QW_QComboBox()
        x_scale_box.addItems(['linear', 'log'])
        x_axis_layout.addRow("Scale", x_scale_box)

        # Y-AXIS
        # Create a group box for the Y-axis
        y_axis_group = QW_QGroupBox("Y-axis")
        layout.addRow(y_axis_group)
        y_axis_layout = QW_QFormLayout()
        y_axis_group.setLayout(y_axis_layout)

        # Make a box for setting the label on the y-axis
        y_label_box = QW_QLineEdit()
        y_axis_layout.addRow("Label", y_label_box)

        # Make a box for setting the range on the y-axis
        y_range_box = DualSpinBox((float, float))
        y_min_box, y_max_box = y_range_box[:]
        y_min_box.setRange(-9999999, 9999999)
        y_max_box.setRange(-9999999, 9999999)
        y_axis_layout.addRow("Range", y_range_box)

        # Make a box for setting the scale on the y-axis
        y_scale_box = QW_QComboBox()
        y_scale_box.addItems(['linear', 'log'])
        y_axis_layout.addRow("Scale", y_scale_box)

        # Return tab
        return(tab, "Figure")

    # This function creates the 'Plots' tab
    def create_plots_tab(self):
        # Create a tab
        tab = QW_QWidget()

        # Create layout
        layout = QW_QFormLayout()
        tab.setLayout(layout)

        # DATA
        # Create a group box for setting the data of the plot
        data_group = QW_QGroupBox("Data")
        layout.addRow(data_group)
        data_layout = QW_QFormLayout()
        data_group.setLayout(data_layout)

        # Make a lineedit for setting the label of the plot
        data_label_box = QW_QLineEdit()
        data_layout.addRow("Label", data_label_box)

        # Make a combobox for setting the x-axis data
        x_data_box = DataColumnBox(self.figure_options.data_table_plugin)
        set_box_value(x_data_box, (0, 0))
        get_modified_box_signal(x_data_box).connect(self.draw_line)
        data_layout.addRow("X-axis", x_data_box)
        self.x_data_box = x_data_box

        # Make a combobox for setting the y-axis data
        y_data_box = DataColumnBox(self.figure_options.data_table_plugin)
        set_box_value(y_data_box, (0, 1))
        get_modified_box_signal(y_data_box).connect(self.draw_line)
        data_layout.addRow("Y-axis", y_data_box)
        self.y_data_box = y_data_box

        # LINE
        # Create a group box for setting the line properties of the plot
        line_group = QW_QGroupBox("Line")
        layout.addRow(line_group)
        line_layout = QW_QFormLayout()
        line_group.setLayout(line_layout)

        # Make a combobox for setting the line style
        line_style_box = QW_QComboBox()
        line_layout.addRow("Style", line_style_box)

        # Make a spinbox for setting the line width
        line_width_box = QW_QDoubleSpinBox()
        line_width_box.setRange(0, 9999999)
        line_width_box.setSuffix(" pts")
        line_layout.addRow("Width", line_width_box)

        # Make a colorbox for setting the line color
        line_color_box = ColorBox()
        line_layout.addRow("Color", line_color_box)

        # MARKER
        # Create a group box for setting the marker properties of the plot
        marker_group = QW_QGroupBox("Marker")
        layout.addRow(marker_group)
        marker_layout = QW_QFormLayout()
        marker_group.setLayout(marker_layout)

        # Make a combobox for setting the marker style
        marker_style_box = QW_QComboBox()
        marker_layout.addRow("Style", marker_style_box)

        # Make a spinbox for setting the marker size
        marker_size_box = QW_QDoubleSpinBox()
        marker_size_box.setRange(0, 9999999)
        marker_size_box.setSuffix(" pts")
        marker_layout.addRow("Size", marker_size_box)

        # Make a colorbox for setting the marker color
        marker_color_box = ColorBox()
        marker_layout.addRow("Color", marker_color_box)

        # Return tab
        return(tab, "Plots")

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


# Create custom class for setting the data column used in plots
class DataColumnBox(BaseBox):
    # Initialize DataColumnBox class
    def __init__(self, data_table_plugin_obj, parent=None, *args, **kwargs):
        # Save provided data_table_obj
        self.data_table_plugin = data_table_plugin_obj
        self.tab_widget = data_table_plugin_obj.tab_widget

        # Call super constructor
        super().__init__(parent)

        # Set up the data column box
        self.init(*args, **kwargs)

    # This function sets up the data column box
    def init(self):
        # Create a layout
        layout = QW_QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create a data table combobox
        tables_box = QW_QComboBox()
        self.tables_box = tables_box
        for i, name in enumerate(self.tab_widget.tabNames()):
            tables_box.addItem(name)
            self.set_tables_box_item_tooltip(i, name)
        layout.addWidget(tables_box)

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

        # Create a label for in between the tables and columns boxes
        sep_label = QW_QLabel(":    ")
        sep_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        layout.addWidget(sep_label)

        # Create a data table column box
        columns_box = QW_QComboBox()
        layout.addWidget(columns_box)
        self.columns_box = columns_box

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
            self.model.columnNameChanged.disconnect(
                self.columns_box.setItemText)
            self.model.columnNameChanged.disconnect(
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
            self.model.columnNameChanged.connect(self.columns_box.setItemText)
            self.model.columnNameChanged.connect(
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
            set_box_value(self.columns_box, -1, int)

        # Remove all columns between first and last+1 from the columns box
        for i in reversed(range(first, last+1)):
            self.columns_box.removeItem(i)

    # This function retrieves the data table and column currently selected
    def get_box_value(self):
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

    # This function sets the data table and column currently selected
    def set_box_value(self, value):
        """
        Sets the new data table and data table column for this data column box,
        using their corresponding indices.

        Parameters
        ----------
        value : tuple of (data_table, data_column)
            Tuple containing the logical indices of the data table and its
            column that must be set.

        """

        set_box_value(self.tables_box, value[0], int)
        set_box_value(self.columns_box, value[1], int)
