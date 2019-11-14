# -*- coding: utf-8 -*-

"""
Data Table Headers
==================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from PyQt5 import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports

# All declaration
__all__ = ['BaseHeaderView', 'HorizontalHeaderView', 'VerticalHeaderView']


# %% CLASS DEFINITIONS
# Define base class for the headers of the data table
class BaseHeaderView(QW.QHeaderView):
    # Signal
    sectionRightClicked = QC.pyqtSignal(int)

    # Initialize BaseHeaderView class
    def __init__(self, orientation, parent):
        # Call super constructor
        super().__init__(orientation, parent)

    # This function sets up the header view
    def init(self, context_menu):
        # Set up default properties
        self.setSectionsClickable(True)
        self.setSectionsMovable(True)
        self.setHighlightSections(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(QC.Qt.CustomContextMenu)

        # Set signal handling
        self.customContextMenuRequested.connect(context_menu)

    # Override mouseClickEvent to select section for left and right clicking
    def mousePressEvent(self, event):
        # If event is right clicking, emit sectionRightClicked signal
        if(event.button() == QC.Qt.RightButton):
            self.sectionRightClicked.emit(self.logicalIndexAt(event.pos()))
        return(super().mousePressEvent(event))


# Horizontal data table header
class HorizontalHeaderView(BaseHeaderView):
    # Initialize HorizontalHeaderView class
    def __init__(self, parent, *args, **kwargs):
        # Call super constructor
        super().__init__(QC.Qt.Horizontal, parent)

        # Set up horizontal header view
        self.init(*args, **kwargs)

    # This function sets up the horizontal header view
    def init(self, *args, **kwargs):
        # Call super init
        super().init(*args, **kwargs)

        # Set up default properties
        self.setSortIndicatorShown(True)
        self.setSectionResizeMode(self.Interactive)


# Vertical data table header
class VerticalHeaderView(BaseHeaderView):
    # Initialize VerticalHeaderView class
    def __init__(self, parent, *args, **kwargs):
        # Call super constructor
        super().__init__(QC.Qt.Vertical, parent)

        # Set up vertical header view
        self.init(*args, **kwargs)

    # This function sets up the vertical header view
    def init(self, *args, **kwargs):
        # Call super init
        super().init(*args, **kwargs)

        # Set up default properties
        self.setSectionResizeMode(self.Fixed)