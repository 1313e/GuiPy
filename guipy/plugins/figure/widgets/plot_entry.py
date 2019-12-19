# -*- coding: utf-8 -*-

"""
Figure Plot Entry
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.plugins.figure.widgets.types.props import PLOT_PROPS
from guipy.widgets import BaseBox, QW_QWidget, get_box_value, set_box_value

# All declaration
__all__ = ['FigurePlotEntry']


# %% CLASS DEFINITIONS
# Create custom class for making a plot entry
# TODO: Allow for individual plots to be toggled (toggled QGroupBox?)
# TODO: Write custom QGroupBox that can have a QComboBox as its title?
class FigurePlotEntry(BaseBox):
    # Signals
    labelChanged = QC.Signal(str)

    # Initialize PlotEntryBox class
    def __init__(self, name, toolbar, parent=None, *args, **kwargs):
        # Save provided FigureToolbar object
        self.toolbar = toolbar
        self.data_table_plugin = toolbar.data_table_plugin
        self.figure = toolbar.canvas.figure
        self.axis = self.figure.gca()

        # Call super constructor
        super().__init__(parent)

        # Set up the plot entry box
        self.init(name, *args, **kwargs)

    # This function sets up the plot entry box
    def init(self, name):
        # Create layout for this plot entry box
        self.create_entry_layout()

        # Connect signals
        self.labelChanged.connect(self.set_line_label)

        # Save that currently no line exists and draw the start line
        self.line = None
        set_box_value(self.data_label_box, name)
        self.draw_plot()

    # This function creates the entry layout
    def create_entry_layout(self):
        # Create layout for this plot entry box
        layout = QW_QFormLayout(self)

        # Define list of all plot props that are needed
        prop_names = ['Data', 'Line', 'Marker']

        # Loop over all required plot props
        for prop_name in prop_names:
            # Obtain the PlotProp class associated with this property
            plot_prop_class = PLOT_PROPS[prop_name]

            # Obtain a dictionary with all requirements of this property
            prop_kwargs = {req: getattr(self, req)
                           for req in plot_prop_class.requirements()}

            # Initialize the property and add to layout
            prop_group = plot_prop_class(**prop_kwargs)
            layout.addRow(prop_group)

            # Register all widgets in this property as instance attributes
            for widget_name, widget in prop_group.widgets.items():
                setattr(self, widget_name, widget)

    # Override closeEvent to remove the plot from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Remove the plot from the figure if it exists
        if self.line in self.axis.lines:
            self.axis.lines.remove(self.line)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function draws the 2D line plot
    @QC.Slot()
    def draw_plot(self):
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
            self.update_plot()
        else:
            self.line.set_xdata(xcol)
            self.line.set_ydata(ycol)

    # This function updates the 2D line plot
    @QC.Slot()
    def update_plot(self):
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
