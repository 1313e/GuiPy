# -*- coding: utf-8 -*-

"""
Styles
======

"""


# %% IMPORTS
# Package imports
from matplotlib import rcParams
from matplotlib.lines import lineMarkers, lineStyles
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW
from guipy.widgets import set_box_value

# All declaration
__all__ = ['LineStyleBox', 'MarkerStyleBox']


# %% CLASS DEFINITIONS
# Make class for setting the linestyle
class LineStyleBox(GW.QComboBox):
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up linestyle box
        self.init()

    # This function sets up the linestyle box
    def init(self):
        # Obtain list with all supported linestyles if not existing already
        if not hasattr(self, 'LINESTYLES'):
            # Create list of all supported linestyles
            linestyles = [(key, value[6:]) for key, value in lineStyles.items()
                          if value != '_draw_nothing']
            linestyles.append(('', 'nothing'))
            linestyles.sort(key=lambda x: x[0])

            # Save as class attribute
            LineStyleBox.LINESTYLES = linestyles

        # Populate this box with all supported linestyles
        for i, (linestyle, tooltip) in enumerate(self.LINESTYLES):
            self.addItem(linestyle)
            self.setItemData(i, tooltip, QC.Qt.ToolTipRole)

        # Set initial value to the default value in MPL
        set_box_value(self, rcParams['lines.linestyle'])

    # Override set_box_value to account for other spellings of 'nothing'
    def set_box_value(self, value, *value_sig):
        # Set value to empty if it uses a different spelling
        if value.lower() in ('none', ' '):
            value = ''
        elif value.lower() in ('dashed', ):
            value = '--'
        elif value.lower() in ('dotted', ):
            value = ':'

        # Call normal method
        set_box_value(self, value, *value_sig, no_custom=True)


# Make class for setting the markerstyle
class MarkerStyleBox(GW.QComboBox):
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up markerstyle box
        self.init()

    # This function sets up the markerstyle box
    def init(self):
        # Obtain list with all supported markerstyles if not existing already
        if not hasattr(self, 'MARKERS'):
            # Create list of all supported markerstyles
            markers = [(key, value) for key, value in lineMarkers.items()
                       if(value != 'nothing' and isinstance(key, str))]
            markers.append(('', 'nothing'))
            markers.sort(key=lambda x: x[0])

            # Save as class attribute
            MarkerStyleBox.MARKERS = markers

        # Populate this box with all supported markerstyles
        for i, (marker, tooltip) in enumerate(self.MARKERS):
            self.addItem(marker)
            self.setItemData(i, tooltip, QC.Qt.ToolTipRole)

        # Set initial value to the default value in MPL
        set_box_value(self, rcParams['lines.marker'])

    # Override set_box_value to account for other spellings of 'nothing'
    def set_box_value(self, value, *value_sig):
        # Set value to empty if it uses a different spelling
        if value.lower() in ('none', ' '):
            value = ''

        # Call normal method
        set_box_value(self, value, *value_sig, no_custom=True)
