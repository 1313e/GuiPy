# -*- coding: utf-8 -*-

"""
Line Type
=========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from matplotlib import rcParams
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.plugins.figure.widgets.types.props import PLOT_PROPS
from guipy.widgets import QW_QWidget, get_box_value, set_box_value

# All declaration
__all__ = ['LineType']


# %% CLASS DEFINITIONS
# Create custom class for making a line plot
# TODO: Allow for individual plots to be toggled (toggled QGroupBox?)
# TODO: Write custom QGroupBox that can have a QComboBox as its title?
class LineType(QW_QWidget):
    # Signals
    labelChanged = QC.Signal(str)

    # Initialize LineType class
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

    # This function sets up the line plot
    def init(self, name):
        # Create layout for this line plot
        self.create_type_layout()

        # Connect signals
        self.labelChanged.connect(self.set_plot_label)

        # Save that currently no line exists
        self.plot = None
        set_box_value(self.data_label_box, name)

        # Set the starting color to be the number of lines already present
        n_lines = len(self.axis.lines)
        color = "C%i" % (n_lines % len(rcParams['axes.prop_cycle']))
        set_box_value(self.line_color_box, color)
        set_box_value(self.marker_color_box, color)

    # This function creates the type layout
    def create_type_layout(self):
        # Create layout for this plot type
        layout = QW_QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

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
        if self.plot in self.axis.lines:
            self.axis.lines.remove(self.plot)

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
        if self.plot not in self.axis.lines:
            self.plot = self.axis.plot(xcol, ycol)[0]
            self.set_plot_label()
            self.update_plot()
        else:
            self.plot.set_xdata(xcol)
            self.plot.set_ydata(ycol)

    # This function updates the 2D line plot
    @QC.Slot()
    def update_plot(self):
        # If line currently exists, update it
        if self.plot is not None:
            # Update line style, width and color
            self.plot.set_linestyle(get_box_value(self.line_style_box))
            self.plot.set_linewidth(get_box_value(self.line_width_box))
            self.plot.set_color(get_box_value(self.line_color_box))

            # Update marker style, size and color
            self.plot.set_marker(get_box_value(self.marker_style_box))
            self.plot.set_markersize(get_box_value(self.marker_size_box))
            self.plot.set_markeredgecolor(get_box_value(self.marker_color_box))
            self.plot.set_markerfacecolor(get_box_value(self.marker_color_box))

    # This function sets the label of a line
    @QC.Slot()
    def set_plot_label(self):
        # If line currently exists, set its label
        if self.plot is not None:
            self.plot.set_label(get_box_value(self.data_label_box))
