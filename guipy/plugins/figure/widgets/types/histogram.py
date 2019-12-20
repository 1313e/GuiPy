# -*- coding: utf-8 -*-

"""
Histogram Type
==============

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
__all__ = ['HistogramType']


# %% CLASS DEFINITIONS
# Create custom class for making a histogram plot
# TODO: Allow for multiple (infinite) data sets to be given, for stacked hists
class HistogramType(BasePlotType):
    """
    Provides the definition of the :class:`~HistogramType` plot type.

    """

    # Class attributes
    NAME = "Histogram"
    PROP_NAMES = ['Data1D', 'Histogram']

    # This function sets up the histogram plot
    def init(self, *args, **kwargs):
        # Create layout for this histogram plot
        super().init(*args, **kwargs)

        # Set the starting color to be the number of containers already present
        n_hists = len(self.axis.containers)
        color = "C%i" % (n_hists % len(rcParams['axes.prop_cycle']))
        set_box_value(self.hist_color_box, color)

    # This function draws the histogram plot
    @QC.Slot()
    def draw_plot(self):
        # Obtain the x column
        try:
            xcol = get_box_value(self.x_data_box)[1]
        # If column cannot be called, return
        except IndexError:
            return

        # If xcol is None, return
        if xcol is None:
            return

#        # Determine if a custom value range is requested
#        value_range = get_box_value(self.hist_range_box)
#        value_range = value_range[1:] if value_range[0] else None

        # As histograms cannot be modified, remove current one and make new one
        self.remove_hist()
        self.axis.hist(
            xcol,
            bins=get_box_value(self.n_bins_box),
            cumulative=get_box_value(self.hist_cumul_box),
            orientation=get_box_value(self.hist_orient_box, str).lower())
        self.plot = self.axis.containers[-1]
        self.set_plot_label(get_box_value(self.data_label_box))
        self.update_plot()

    # This function updates the histogram plot
    @QC.Slot()
    def update_plot(self):
        # If histogram currently exists, update it
        if self.plot is not None:
            # Update bin colors
            for patch in self.plot.patches:
                patch.set_color(get_box_value(self.hist_color_box))

    # This function removes the histogram from the figure
    @QC.Slot()
    def remove_hist(self):
        # Remove the plot from the figure if it exists
        if self.plot in self.axis.containers:
            for patch in self.plot.patches:
                self.axis.patches.remove(patch)
            self.axis.containers.remove(self.plot)

    # Override closeEvent to remove the plot from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Remove the plot from the figure if it exists
        self.remove_hist()

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function sets the label of a plot
    @QC.Slot(str)
    def set_plot_label(self, label):
        # If line currently exists, set its label
        if self.plot is not None:
            self.plot.set_label(label)
