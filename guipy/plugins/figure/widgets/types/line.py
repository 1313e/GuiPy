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
from guipy.plugins.figure.widgets.types import BasePlotType
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['LineType']


# %% CLASS DEFINITIONS
# Create custom class for making a line plot
class LineType(BasePlotType):
    """
    Provides the definition of the :class:`~LineType` plot type.

    """

    # Class attributes
    NAME = "Line"
    PREFIX = "line"
    AXIS_TYPE = "2D"
    PROP_NAMES = ['Data2D', 'Line', 'LineMarker']

    # This function sets up the line plot
    def init(self, *args, **kwargs):
        # Create layout for this line plot
        super().init(*args, **kwargs)

        # Set the starting color to be the number of lines already present
        n_lines = len(self.axis.lines)
        color = "C%i" % (n_lines % len(rcParams['axes.prop_cycle']))
        set_box_value(self.line_color_box, color)
        set_box_value(self.marker_color_box, color)

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
            # Make and update plot
            self.plot = self.axis.plot(xcol, ycol)[0]
            set_box_value(self.data_label_box, self.plot.get_label())
            self.update_plot()

            # If the figure currently has no title, set it
            title_box = self.toolbar.options_dialog.title_box[0]
            if not get_box_value(title_box):
                set_box_value(title_box, "%s vs. %s" % (xcol.name, ycol.name))

            # If the figure currently has no axes labels, set them
            x_label_box = self.toolbar.options_dialog.x_label_box[0]
            y_label_box = self.toolbar.options_dialog.y_label_box[0]
            if not (get_box_value(x_label_box) or get_box_value(y_label_box)):
                set_box_value(x_label_box, xcol.name)
                set_box_value(y_label_box, ycol.name)
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

    # Override closeEvent to remove the plot from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Remove the plot from the figure if it exists
        if self.plot in self.axis.lines:
            self.axis.lines.remove(self.plot)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function sets the label of a plot
    @QC.Slot(str)
    def set_plot_label(self, label):
        # If line currently exists, set its label
        if self.plot is not None:
            self.plot.set_label(label)
