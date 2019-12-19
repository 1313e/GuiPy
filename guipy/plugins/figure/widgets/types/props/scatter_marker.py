# -*- coding: utf-8 -*-

"""
Scatter Marker Property
=======================

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
__all__ = ['ScatterMarkerProp']


# %% CLASS DEFINITIONS
# Define 'ScatterMarker' plot property
class ScatterMarkerProp(BasePlotProp):
    # Class attributes
    NAME = "ScatterMarker"
    DISPLAY_NAME = "Marker"
    REQUIREMENTS = ['update_plot']
    WIDGET_NAMES = ['marker_style_box', 'marker_size_box', 'marker_color_box']

    # This function creates and returns a line style box
    def marker_style_box(self):
        # Obtain list with all supported markerstyles if not existing already
        if not hasattr(self, 'markerstyles'):
            # Create list of all supported markerstyles
            markers = [(key, value) for key, value in lineMarkers.items()
                       if(value != 'nothing' and isinstance(key, str))]
            markers.append(('', 'nothing'))
            markers.sort(key=lambda x: x[0])

            # Save as class attribute
            ScatterMarkerProp.markers = markers

        # Make combobox for markerstyles
        marker_style_box = QW_QComboBox()
        marker_style_box.setToolTip("Marker to be used for this plot")

        # Populate box with all supported linestyles
        for i, (marker, tooltip) in enumerate(self.markers):
            marker_style_box.addItem(marker)
            marker_style_box.setItemData(i, tooltip, QC.Qt.ToolTipRole)

        # Set initial value to the default value in MPL
        set_box_value(marker_style_box, rcParams['scatter.marker'])

        # Connect signals
        get_modified_box_signal(marker_style_box).connect(self.update_plot)

        # Return name and box
        return('Style', marker_style_box)

    # This function creates and returns a marker size box
    def marker_size_box(self):
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
        # Make a color box
        marker_color_box = ColorBox()

        # Connect signals
        get_modified_box_signal(marker_color_box).connect(self.update_plot)

        # Return name and box
        return('Color', marker_color_box)
