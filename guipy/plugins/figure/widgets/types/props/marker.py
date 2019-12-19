# -*- coding: utf-8 -*-

"""
Marker Property
===============

"""


# %% IMPORTS
# Package imports
from matplotlib import rcParams
from matplotlib.lines import lineMarkers
from qtpy import QtCore as QC

# GuiPy imports
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.widgets import (
    ColorBox, QW_QComboBox, QW_QDoubleSpinBox, get_modified_box_signal,
    set_box_value)

# All declaration
__all__ = ['LineMarkerProp', 'ScatterMarkerProp']


# %% CLASS DEFINITIONS
# Define 'Marker' plot property
class MarkerProp(BasePlotProp):
    # Class attributes
    DISPLAY_NAME = "Marker"
    REQUIREMENTS = ['update_plot']
    WIDGET_NAMES = ['marker_style_box', 'marker_size_box', 'marker_color_box']

    # This function creates and returns a line style box
    def marker_style_box(self):
        """
        Creates a widget box for setting the style of the marker and returns
        it.

        """

        # Obtain list with all supported markerstyles if not existing already
        if not hasattr(self, 'MARKERS'):
            # Create list of all supported markerstyles
            markers = [(key, value) for key, value in lineMarkers.items()
                       if(value != 'nothing' and isinstance(key, str))]
            markers.append(('', 'nothing'))
            markers.sort(key=lambda x: x[0])

            # Save as class attribute
            MarkerProp.MARKERS = markers

        # Make combobox for markerstyles
        marker_style_box = QW_QComboBox()
        marker_style_box.setToolTip("Marker to be used for this plot")

        # Populate box with all supported linestyles
        for i, (marker, tooltip) in enumerate(self.MARKERS):
            marker_style_box.addItem(marker)
            marker_style_box.setItemData(i, tooltip, QC.Qt.ToolTipRole)

        # Set initial value to the default value in MPL
        set_box_value(marker_style_box, self.DEFAULT_MARKER)

        # Connect signals
        get_modified_box_signal(marker_style_box).connect(self.update_plot)

        # Return name and box
        return('Style', marker_style_box)

    # This function creates and returns a marker size box
    def marker_size_box(self):
        """
        Creates a widget box for setting the size of the marker and returns it.

        """

        # Make a double spinbox for markersize
        marker_size_box = QW_QDoubleSpinBox()
        marker_size_box.setToolTip("Size of the plotted markers")
        marker_size_box.setRange(0, 9999999)
        marker_size_box.setSuffix(" pts")

        # Set initial value to the default value in MPL
        set_box_value(marker_size_box, rcParams['lines.markersize'])

        # Connect signals
        get_modified_box_signal(marker_size_box).connect(self.update_plot)

        # Return name and box
        return('Size', marker_size_box)

    # This function creates and returns a marker color box
    def marker_color_box(self):
        """
        Creates a widget box for setting the color of the marker and returns
        it.

        """

        # Make a color box
        marker_color_box = ColorBox()

        # Connect signals
        get_modified_box_signal(marker_color_box).connect(self.update_plot)

        # Return name and box
        return('Color', marker_color_box)


# Define 'LineMarker' plot property
class LineMarkerProp(MarkerProp):
    """
    Provides the definition of the :class:`~LineMarkerProp` plot property,
    specifically used for line plots.

    This property contains boxes for setting the marker style, marker size and
    marker color.

    """

    # Class attributes
    NAME = "LineMarker"
    DEFAULT_MARKER = rcParams['lines.marker']


# Define 'ScatterMarker' plot property
class ScatterMarkerProp(MarkerProp):
    """
    Provides the definition of the :class:`~ScatterMarkerProp` plot property,
    specifically used for scatter plots.

    This property contains boxes for setting the marker style, marker size and
    marker color.

    """

    # Class attributes
    NAME = "ScatterMarker"
    DEFAULT_MARKER = rcParams['scatter.marker']
