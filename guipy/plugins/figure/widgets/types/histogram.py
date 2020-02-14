# -*- coding: utf-8 -*-

"""
Histogram Type
==============

"""


# %% IMPORTS
# Built-in imports

# Package imports
import numpy as np
import pandas as pd
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import CONFIG
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

        # Set current hist_kwargs to None
        self.hist_kwargs = None

    # This function is called whenever a new histogram data tab is added
    @QC.Slot(int)
    def hist_tab_added(self, index):
        """
        This slot is automatically called whenever a new histogram data tab
        with `index` has been added, and is used for initializing certain
        aspects of this tab.

        """

        # Obtain the number of data tabs already present
        n_tabs = self.multi_data_box.count()

        # Use this number to cycle through MPL's color cycler
        color = "C%i" % (n_tabs-1 % len(CONFIG['rcParams']['axes.prop_cycle']))
        set_box_value(self.multi_data_box, color, index, 'hist_color_box')

    # This function draws the histogram plot
    # TODO: Allow for the bin-width and a single bin-edge to be given instead?
    @QC.Slot()
    def draw_plot(self):
        # Obtain the x columns
        try:
            xcols = get_box_value(self.multi_data_box, 'x_data_box', 1)
        # If any column cannot be called, return
        except IndexError:
            self.remove_plot()
            return

        # If any of the xcols contains None, return as well
        if pd.isna(xcols).any():
            self.remove_plot()
            return

#        # Determine if a custom value range is requested
#        value_range = get_box_value(self.hist_range_box)
#        value_range = value_range[1:] if value_range[0] else None

        # Obtain the histogram keyword arguments
        bins = get_box_value(self.n_bins_box)
        hist_kwargs = {
            'bins': bins if bins else self.n_bins_box.specialValueText(),
            'cumulative': get_box_value(self.hist_cumul_box),
            'orientation': get_box_value(self.hist_orient_box, str).lower()}

        # Check if this histogram should be drawn
        if self.plot is not None:
            # Check all arguments except data
            if not all(map(lambda k: (hist_kwargs[k] == self.hist_kwargs[k]),
                           hist_kwargs.keys())):
                pass

            # If all are the same, check data
            elif((len(xcols) == len(self.hist_kwargs['xcols'])) and
                 all(map(np.array_equal, xcols, self.hist_kwargs['xcols']))):
                return

        # As histograms cannot be modified, remove current one
        self.remove_plot()

        # Make a new histogram
        self.axis.hist(xcols, **hist_kwargs)

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

        # Save what arguments were used for this histogram
        hist_kwargs['xcols'] = xcols
        self.hist_kwargs = hist_kwargs

    # This function updates the histogram plot
    @QC.Slot()
    def update_plot(self):
        # Draw the plot
        self.draw_plot()

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
    def remove_plot(self):
        """
        Removes all histograms handled by this instance from the current
        figure.

        """

        # Remove the plots from the figure if they exist
        if self.plot is not None:
            for plot in self.plot:
                # Remove all patches of this histogram
                for patch in plot.patches:
                    self.axis.patches.remove(patch)

                # And remove the container for it as well
                self.axis.containers.remove(plot)

            # Set plot and hist_kwargs to None
            self.plot = None
            self.hist_kwargs = None

    # This function sets the label of a plot
    @QC.Slot(int, str)
    def set_plot_label(self, index, label):
        # If histogram currently exists, set its associated label
        if self.plot is not None:
            self.plot[index].set_label(label)
