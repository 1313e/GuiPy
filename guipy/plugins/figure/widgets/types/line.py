# -*- coding: utf-8 -*-

"""
Line Type
=========

"""


# %% IMPORTS
# Built-in imports

# Package imports
import numpy as np
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
    PROP_NAMES = [*BasePlotType.PROP_NAMES, 'Data1or2D', 'Line', 'LineMarker']

    # This function sets up the line plot
    def init(self, *args, **kwargs):
        # Create layout for this line plot
        super().init(*args, **kwargs)

        # Set the starting color to be the number of lines already present
        n_lines = len(self.axis.lines)
        color = "C%i" % (n_lines % len(self.get_option('rcParams',
                                                       'axes.prop_cycle')))
        set_box_value(self.line_color_box, color)
        set_box_value(self.marker_color_box, color)

    # This function draws the 2D line plot
    @QC.Slot()
    def draw_plot(self):
        # Obtain the x and y columns
        try:
            # Obtain y column
            ycol = get_box_value(self.y_data_box)[1]

            # Check if the x column is currently enabled
            if get_box_value(self.x_data_box, bool):
                # If so, obtain xcol
                xcol = get_box_value(self.x_data_box)[1][1]
            else:
                # If not, xcol is a NumPy array
                xcol = np.arange(len(ycol)) if ycol is not None else None

        # If any column cannot be called, return
        except IndexError:
            self.remove_plot()
            return

        # If either xcol or ycol is None, return
        if xcol is None or ycol is None:
            self.remove_plot()
            return

        # If xcol and ycol are not the same shape, return
        if(len(xcol) != len(ycol)):
            self.remove_plot()
            return

        # If the current saved line is not already in the figure, make one
        if self.plot not in self.axis.lines:
            # Make and update plot
            self.plot = self.axis.plot(xcol, ycol)[0]

            # Obtain label currently set in label box
            label = get_box_value(self.data_label_box)

            # If label is not empty, reuse it in the plot
            if label:
                self.plot.set_label(label)
            # Else, obtain its label from MPL
            else:
                set_box_value(self.data_label_box, self.plot.get_label())

            # If the figure currently has no title, set it
            xname = getattr(xcol, 'name', 'index')
            yname = getattr(ycol, 'name')
            title_box = self.toolbar.options_dialog.title_box[0]
            if not get_box_value(title_box):
                set_box_value(title_box, "%s vs. %s" % (xname, yname))

            # If the figure currently has no axes labels, set them
            x_label_box = self.toolbar.options_dialog.x_label_box[0]
            y_label_box = self.toolbar.options_dialog.y_label_box[0]
            if not (get_box_value(x_label_box) or get_box_value(y_label_box)):
                set_box_value(x_label_box, xname)
                set_box_value(y_label_box, yname)

        # If it does exist, check if it requires updating
        else:
            # Obtain the data currently used for this plot
            xcol_cur = self.plot.get_xdata()
            ycol_cur = self.plot.get_ydata()

            # If there are differences, update plot
            if not (xcol_cur == xcol).all():
                self.plot.set_xdata(xcol)
            if not (ycol_cur == ycol).all():
                self.plot.set_ydata(ycol)

    # This function updates the 2D line plot
    @QC.Slot()
    def update_plot(self):
        # Draw the plot
        self.draw_plot()

        # If line currently exists, update it
        if self.plot is not None:
            # Set plot label
            self.plot.set_label(get_box_value(self.data_label_box))

            # Update line style, width and color
            self.plot.set_linestyle(get_box_value(self.line_style_box))
            self.plot.set_linewidth(get_box_value(self.line_width_box))
            self.plot.set_color(get_box_value(self.line_color_box))

            # Update marker style, size and color
            self.plot.set_marker(get_box_value(self.marker_style_box))
            self.plot.set_markersize(get_box_value(self.marker_size_box))
            self.plot.set_markeredgecolor(get_box_value(self.marker_color_box))
            self.plot.set_markerfacecolor(get_box_value(self.marker_color_box))

    # This function removes the 2D line plot
    @QC.Slot()
    def remove_plot(self):
        # Remove the plot from the figure if it exists
        if self.plot in self.axis.lines:
            self.axis.lines.remove(self.plot)

            # Set plot to None
            self.plot = None
