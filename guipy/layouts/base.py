# -*- coding: utf-8 -*-

"""
Base Layouts
============
Provides a collection of custom :class:`~PyQt5.QtWidgets.QLayout` base classes
that allow for certain layouts to be standardized.

"""


# %% IMPORTS
# Package imports
from qtpy import QtWidgets as QW

# All declaration
__all__ = ['QW_QFormLayout', 'QW_QGridLayout', 'QW_QHBoxLayout',
           'QW_QVBoxLayout']


# %% CLASS DEFINITIONS
# Make subclass of QW.QFormLayout to add separator function
class QW_QFormLayout(QW.QFormLayout):
    # This function adds a horizontal separator to the layout
    def addSeparator(self):
        # Create frame object
        frame = QW.QFrame()

        # Set the frame shape
        frame.setFrameShape(frame.HLine)
        frame.setFrameShadow(frame.Sunken)

        # Add frame to this layout
        self.addRow(frame)


# Make subclass of QW.QGridLayout to add separator function
class QW_QGridLayout(QW.QGridLayout):
    # This function adds a separator to the layout
    def addSeparator(self, *, row=None, column=None):
        # Create frame object
        frame = QW.QFrame()

        # Set the frame shape
        frame.setFrameShape(frame.VLine if row is None else frame.HLine)
        frame.setFrameShadow(frame.Sunken)

        # Add frame to this layout
        if row is None:
            self.addWidget(frame, 0, column, -1, 1)
        else:
            self.addWidget(frame, row, 0, 1, -1)


# Make subclass of QW.QHBoxLayout to add separator function
class QW_QHBoxLayout(QW.QHBoxLayout):
    # This function adds a vertical separator to the layout
    def addSeparator(self):
        # Create frame object
        frame = QW.QFrame()

        # Set the frame shape
        frame.setFrameShape(frame.VLine)
        frame.setFrameShadow(frame.Sunken)

        # Add frame to this layout
        self.addWidget(frame)


# Make subclass of QW.QVBoxLayout to add separator function
class QW_QVBoxLayout(QW.QVBoxLayout):
    # This function adds a horizontal separator to the layout
    def addSeparator(self):
        # Create frame object
        frame = QW.QFrame()

        # Set the frame shape
        frame.setFrameShape(frame.HLine)
        frame.setFrameShadow(frame.Sunken)

        # Add frame to this layout
        self.addWidget(frame)
