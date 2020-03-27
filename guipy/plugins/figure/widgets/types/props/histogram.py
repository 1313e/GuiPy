# -*- coding: utf-8 -*-

"""
Histogram Property
==================

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.plugins.figure.widgets.types.props.data import (
    Data1DProp, MultiDataNDProp)
from guipy.widgets import get_box_value, get_modified_box_signal, set_box_value

# All declaration
__all__ = ['HistogramProp', 'MultiHistDataProp']


# %% CLASS DEFINITIONS
# Define 'Histogram' plot property
class HistogramProp(BasePlotProp):
    """
    Provides the definition of the :class:`~HistogramProp` plot property.

    This property contains boxes for setting the number of bins, the value
    range, and the histogram bar colors.

    """

    # Class attributes
    NAME = "Histogram"
    DISPLAY_NAME = "Histogram"
    WIDGET_NAMES = [*BasePlotProp.WIDGET_NAMES, 'n_bins_box',
                    'hist_orient_box', 'hist_cumul_box']

    # This function creates and returns a bins box
    def n_bins_box(self):
        """
        Creates a widget box for setting the number of bins in a histogram and
        returns it.

        """

        # Make spinbox for bin count
        n_bins_box = GW.QSpinBox()
        n_bins_box.setToolTip("Number of bins used for this histogram. Set to "
                              "'auto' to automatically determine this number")
        n_bins_box.setRange(0, 100)
        n_bins_box.setSpecialValueText('auto')

        # Set initial value to 'auto'
        set_box_value(n_bins_box, 0)

        # Return name and box
        return('# of bins', n_bins_box)

    # This function creates a histogram cumulative box
    def hist_cumul_box(self):
        """
        Creates a widget box for setting the cumulative property of this
        histogram and returns it.

        """

        # Make a checkbox
        hist_cumul_box = GW.QCheckBox('Cumulative')
        hist_cumul_box.setToolTip("Toggle the use of a cumulative histogram")

        # Return name and box
        return(hist_cumul_box,)

    # This function creates a histogram orientation box
    def hist_orient_box(self):
        """
        Creates a widget box for setting the orientation property of this
        histogram and returns it.

        """

        # Make a multi radiobutton
        hist_orient_box = GW.MultiRadioButton(['Horizontal', 'Vertical'])
        hist_orient_box.setToolTip("The orientation of the histogram")
        set_box_value(hist_orient_box, 'Vertical')

        # Return name and box
        return('Orientation', hist_orient_box)


# Define 'HistData' plot property
class HistDataProp(Data1DProp):
    """
    Provides the definition of the :class:`~HistDataProp` plot property.

    This property contains boxes for setting the label; X-axis data and color
    for an individual histogram.

    """

    # Class attributes
    NAME = "HistData"
    WIDGET_NAMES = [*Data1DProp.WIDGET_NAMES, 'hist_color_box']

    # This function creates a histogram color box
    def hist_color_box(self):
        """
        Creates a widget box for setting the color of this histogram and
        returns it.

        """

        # Make a color box
        hist_color_box = GW.ColorBox()

        # Return name and box
        return('Color', hist_color_box)


# Define custom class for setting the data used in the histogram
class MultiHistDataProp(MultiDataNDProp):
    """
    Provides the definition of the :class:`~MultiHistDataProp` plot property.

    This property contains a tab widget with multiple :class`~HistDataProp`
    properties.

    """

    # Class attributes
    NAME = "MultiHistData"
    REQUIREMENTS = [*MultiDataNDProp.REQUIREMENTS, *HistDataProp.REQUIREMENTS,
                    'hist_tab_added']

    # Initialize hist data property
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(HistDataProp, *args, **kwargs)

        # Connect signals
        self.tab_widget.tabWasInserted.connect(self.hist_tab_added)


# Define custom class for setting the value range of a histogram
class HistRangeBox(GW.BaseBox):
    # Signals
    rangeChanged = QC.Signal(float, float)

    # Initialize instance of HistRangeBox
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up histogram range box
        self.init()

    # This function sets up the histogram range box
    def init(self):
        # Make layout for setting the value range of the histogram
        hist_range_layout = GL.QHBoxLayout(self)
        hist_range_layout.setContentsMargins(0, 0, 0, 0)

        # Make a box for setting the value range of the histogram
        # TODO: Maybe use dual lineedits instead to eliminate range problem?
        hist_range_box = GW.DualSpinBox((float, float),
                                        r"<html>&le; X &le;</html>")
        x_min_box, x_max_box = hist_range_box[:]
        x_min_box.setRange(-9999999, 9999999)
        x_min_box.setToolTip("Minimum value to be included in the histogram")
        x_max_box.setRange(-9999999, 9999999)
        x_max_box.setToolTip("Maximum value to be included in the histogram")
        set_box_value(hist_range_box, (0, 0))
        hist_range_box.setEnabled(False)
        self.range_box = hist_range_box

        # Make a checkbox for enabling/disabling the use of this range
        hist_range_flag = GW.QCheckBox()
        hist_range_flag.setToolTip("Toggle the use of a manual histogram value"
                                   " range")
        set_box_value(hist_range_flag, False)
        self.range_flag = hist_range_flag

        # Connect signals for hist_range_flag
        get_modified_box_signal(hist_range_flag).connect(
            hist_range_box.setEnabled)

        # Add everything together
        hist_range_layout.addWidget(hist_range_flag)
        hist_range_layout.addWidget(hist_range_box)

    # This function retrieves a value of this special box
    def get_box_value(self, *args, **kwargs):
        return(get_box_value(self.range_flag), *get_box_value(self.range_box))

    # This function sets the value of this special box
    def set_box_value(self, value, *args, **kwargs):
        set_box_value(self.range_box, value, *args, **kwargs)
