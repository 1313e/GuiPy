# -*- coding: utf-8 -*-

"""
Dock Widget
===========
Provides the base definition of the dock widgets used in *GuiPy*.

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW

# All declaration
__all__ = ['BaseDockWidget']


# %% CLASS DEFINITIONS
# Make base class for dock widgets
class BaseDockWidget(GW.QDockWidget):
    # Signals
    dockClosed = QC.Signal()

    # Override closeEvent to emit a signal whenever the dock is closed
    def closeEvent(self, *args, **kwargs):
        # Emit dockClosed signal
        self.dockClosed.emit()

        # Call super event
        super().closeEvent(*args, **kwargs)
