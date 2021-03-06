# -*- coding: utf-8 -*-

"""
Marker Property
===============

"""


# %% IMPORTS
# Package imports
from matplotlib import rcParams

# GuiPy imports
from guipy import widgets as GW
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.widgets import set_box_value

# All declaration
__all__ = ['LineMarkerProp', 'ScatterMarkerProp']


# %% CLASS DEFINITIONS
# Define 'Marker' plot property
class MarkerProp(BasePlotProp):
    # Class attributes
    DISPLAY_NAME = "Marker"
    WIDGET_NAMES = [*BasePlotProp.WIDGET_NAMES, 'marker_style_box',
                    'marker_size_box', 'marker_color_box']

    # This function creates and returns a line style box
    def marker_style_box(self):
        """
        Creates a widget box for setting the style of the marker and returns
        it.

        """

        # Make combobox for markerstyles
        marker_style_box = GW.MarkerStyleBox()
        marker_style_box.setToolTip("Marker to be used for this plot")

        # Set initial value to the default value in MPL
        set_box_value(marker_style_box, self.default_marker)

        # Return name and box
        return('Style', marker_style_box)

    # This function creates and returns a marker size box
    def marker_size_box(self):
        """
        Creates a widget box for setting the size of the marker and returns it.

        """

        # Make a double spinbox for markersize
        marker_size_box = GW.QDoubleSpinBox()
        marker_size_box.setToolTip("Size of the plotted markers")
        marker_size_box.setRange(0, 9999999)
        marker_size_box.setSuffix(" pts")

        # Set initial value to the default value in MPL
        set_box_value(marker_size_box, rcParams['lines.markersize'])

        # Return name and box
        return('Size', marker_size_box)

    # This function creates and returns a marker color box
    def marker_color_box(self):
        """
        Creates a widget box for setting the color of the marker and returns
        it.

        """

        # Make a color box
        marker_color_box = GW.ColorBox()
        marker_color_box.setToolTip("Color to be used for this marker")

        # Connect 'applying' signal
        self.options.applying.connect(marker_color_box.set_default_color)

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

    # This property holds the default marker used for line plots
    @property
    def default_marker(self):
        return(rcParams['lines.marker'])


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

    # This property holds the default marker used for scatter plots
    @property
    def default_marker(self):
        return(rcParams['scatter.marker'])
