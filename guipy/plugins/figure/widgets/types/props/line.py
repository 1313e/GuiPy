# -*- coding: utf-8 -*-

"""
Line Property
=============

"""


# %% IMPORTS
# Package imports
from matplotlib.lines import lineStyles
from qtpy import QtCore as QC

# GuiPy imports
from guipy import widgets as GW
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.widgets import set_box_value

# All declaration
__all__ = ['LineProp']


# %% CLASS DEFINITIONS
# Define 'Line' plot property
class LineProp(BasePlotProp):
    """
    Provides the definition of the :class:`~LineProp` plot property.

    This property contains boxes for setting the line style, line width and
    line color.

    """

    # Class attributes
    NAME = "Line"
    DISPLAY_NAME = "Line"
    WIDGET_NAMES = [*BasePlotProp.WIDGET_NAMES, 'line_style_box',
                    'line_width_box', 'line_color_box']

    # This function creates and returns a line style box
    def line_style_box(self):
        """
        Creates a widget box for setting the style of this line plot and
        returns it.

        """

        # Obtain list with all supported linestyles if not existing already
        if not hasattr(self, 'LINESTYLES'):
            # Create list of all supported linestyles
            linestyles = [(key, value[6:]) for key, value in lineStyles.items()
                          if value != '_draw_nothing']
            linestyles.append(('', 'nothing'))
            linestyles.sort(key=lambda x: x[0])

            # Save as class attribute
            LineProp.LINESTYLES = linestyles

        # Make combobox for linestyles
        line_style_box = GW.QComboBox()
        line_style_box.setToolTip("Linestyle to be used for this line plot")

        # Populate box with all supported linestyles
        for i, (linestyle, tooltip) in enumerate(self.LINESTYLES):
            line_style_box.addItem(linestyle)
            line_style_box.setItemData(i, tooltip, QC.Qt.ToolTipRole)

        # Set initial value to the default value in MPL
        set_box_value(line_style_box,
                      self.get_option('rcParams', 'lines.linestyle'))

        # Return name and box
        return('Style', line_style_box)

    # This function creates and returns a line width box
    def line_width_box(self):
        """
        Creates a widget box for setting the width of this line plot and
        returns it.

        """

        # Make a double spinbox for linewidth
        line_width_box = GW.QDoubleSpinBox()
        line_width_box.setToolTip("Width of the plotted line")
        line_width_box.setRange(0, 9999999)
        line_width_box.setSuffix(" pts")

        # Set initial value to the default value in MPL
        set_box_value(line_width_box,
                      self.get_option('rcParams', 'lines.linewidth'))

        # Return name and box
        return('Width', line_width_box)

    # This function creates a line color box
    def line_color_box(self):
        """
        Creates a widget box for setting the color of this line plot and
        returns it.

        """

        # Make a color box
        line_color_box = GW.ColorBox()

        # Connect 'applying' signal
        self.options.applying.connect(line_color_box.set_default_color)

        # Return name and box
        return('Color', line_color_box)
