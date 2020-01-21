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
class HistogramType(BasePlotType):
    """
    Provides the definition of the :class:`~HistogramType` plot type.

    """

    # Class attributes
    NAME = "Histogram"
    PREFIX = "hist"
    AXIS_TYPE = "2D"
    PROP_NAMES = ['MultiHistData', 'Histogram']

    # Signals
    dataLabelChanged = QC.Signal(int, str)

    # This function sets up the histogram plot
    def init(self, *args, **kwargs):
        # Create layout for this histogram plot
        super().init(*args, **kwargs)

        # Manually call hist_tab_added
        self.hist_tab_added(0)

    # This function is called whenever a new histogram data tab is added
    @QC.Slot(int)
    def hist_tab_added(self, index):
        # Obtain the number of data tabs already present
        n_tabs = self.multi_data_box.count()

        # Use this number to cycle through MPL's color cycler
        color = "C%i" % (n_tabs-1 % len(rcParams['axes.prop_cycle']))
        set_box_value(self.multi_data_box, color, index, 'hist_color_box')

    # This function draws the histogram plot
    @QC.Slot()
    def draw_plot(self):
        # Obtain the x columns
        try:
            xcols = get_box_value(self.multi_data_box, 'x_data_box', 1)
        # If any column cannot be called, return
        except IndexError:
            return

        # If any of the xcols contains None, return as well
        if None in xcols:
            return

#        # Determine if a custom value range is requested
#        value_range = get_box_value(self.hist_range_box)
#        value_range = value_range[1:] if value_range[0] else None

        # As histograms cannot be modified, remove current one
        self.remove_hist()

        # Make a new histogram
        self.axis.hist(
            xcols,
            bins=get_box_value(self.n_bins_box),
            cumulative=get_box_value(self.hist_cumul_box),
            orientation=get_box_value(self.hist_orient_box, str).lower())

        # Save the made histogram(s)
        self.plot = self.axis.containers[-len(xcols):]

        # Loop over all labels for all data sets
        for i, label in enumerate(get_box_value(self.multi_data_box,
                                                'data_label_box')):
            # If label is not empty, reuse it in the plot
            if label:
                self.set_plot_label(i, label)
            # Else, obtain its label from MPL
            else:
                label = self.plot[i].get_label()
                set_box_value(self.multi_data_box, label, i, 'data_label_box')

        # Update the plot
        self.update_plot()

    # This function updates the histogram plot
    @QC.Slot()
    def update_plot(self):
        # If histograms currently exist, update them
        if self.plot is not None:
            for i, plot in enumerate(self.plot):
                # Obtain color set for this histogram
                color = get_box_value(self.multi_data_box, i, 'hist_color_box')

                # Update bin colors
                for patch in plot.patches:
                    patch.set_color(color)

    # This function removes the histogram from the figure
    @QC.Slot()
    def remove_hist(self):
        # Remove the plots from the figure if they exist
        if self.plot is not None:
            for plot in self.plot:
                # Remove all patches of this histogram
                for patch in plot.patches:
                    self.axis.patches.remove(patch)

                # And remove the container for it as well
                self.axis.containers.remove(plot)

    # Override closeEvent to remove the plots from the figure when closed
    def closeEvent(self, *args, **kwargs):
        # Remove the plots from the figure if they exist
        self.remove_hist()

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function sets the label of a plot
    @QC.Slot(int, str)
    def set_plot_label(self, index, label):
        # If histogram currently exists, set its label
        if self.plot[index] is not None:
            self.plot[index].set_label(label)
