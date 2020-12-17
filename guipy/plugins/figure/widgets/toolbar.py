# -*- coding: utf-8 -*-

"""
Figure Toolbar
==============

"""


# %% IMPORTS
# Built-in imports
from os import path

# Package imports
from matplotlib import cbook
from matplotlib.backend_bases import _default_filetypes, NavigationToolbar2
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW
from guipy.config import FILE_FILTERS

# All declaration
__all__ = ['FigureToolbar']


# %% CLASS DEFINITIONS
# Custom FigureToolbar class
class FigureToolbar(NavigationToolbar2QT, GW.QToolBar):
    # Signals
    status_message = QC.Signal(str)

    # Initialize FigureToolbar class
    def __init__(self, canvas, options, figure_widget_obj):
        # Save provided FigureWidget object
        self.options = options
        self.figure_widget = figure_widget_obj

        # Initialize empty actions dict
        self._actions = {}

        # Call super constructors
        GW.QToolBar.__init__(self, "Figure Toolbar", parent=figure_widget_obj)
        NavigationToolbar2.__init__(self, canvas)

    # This function sets up the figure toolbar
    def _init_toolbar(self):
        # Create pointer in figure manager to this toolbar
        self.canvas.manager.toolbar = self

        # Store the base dir for images for NavigationToolbar2QT
        self.basedir = str(cbook._get_data_path('images'))

        # Determine what icon color to use
        background_color = self.palette().color(self.backgroundRole())
        foreground_color = self.palette().color(self.foregroundRole())
        icon_color = (foreground_color
                      if background_color.value() < 128 else None)

        # Create list of info for the toolbuttons
        button_info = [
            ('Home', 'Reset to original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan with left button, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Options', 'Add, remove, and edit figure elements',
             'qt4_editor_options', 'options'),
            ('Save', 'Save the figure', 'filesave', 'save_figure')]

        # Loop over all items in button_info and create the actions
        for text, tooltip, image_file, func in button_info:
            # If text is None, a separator is required
            if text is None:
                self.addSeparator()
            # Else, create an action
            else:
                # Create action
                action = GW.QAction(
                    self, text,
                    tooltip=tooltip,
                    icon=self._icon(image_file+'.png', icon_color),
                    triggered=getattr(self, func))
                self.addAction(action)

                # Add action to self._actions
                self._actions[func] = action

                # Make zoom and pan checkable
                if func in ['zoom', 'pan']:
                    action.setCheckable(True)

        # Add separator
        self.addSeparator()

        # Add a label that contains the coordinates of the figure
        coord_label = GW.QLabel('')
        coord_label.setSizePolicy(QW.QSizePolicy.Expanding,
                                  QW.QSizePolicy.Ignored)
        self.addWidget(coord_label)
        self.status_message.connect(coord_label.setText)

    # Override set_message to just emit the signal
    def set_message(self, s):
        self.status_message.emit(s)

    # Override save_figure to use GuiPy's dialogs
    def save_figure(self):
        # Get name of this figure
        name = self.figure_widget.tab_name

        # Open the file saving system
        filepath, selected_filter = GW.getSaveFileName(
            parent=self.figure_widget,
            caption="Save figure %r to..." % (name),
            basedir=name,
            filters=list(map(lambda x: '.'+x, _default_filetypes.keys())),
            initial_filter='.png')

        # If filepath is not empty, save figure
        if filepath:
            # Obtain the ext of the filepath
            ext = path.splitext(filepath)[1]

            # If ext is empty, check what filter was used
            if not ext:
                # If "All (Supported) Files" was not used, get ext from filter
                if not selected_filter.startswith("All "):
                    ext = FILE_FILTERS[selected_filter]
                # Else, set it to '.png'
                else:
                    ext = '.png'

                # Add extension to filepath
                filepath += ext

            # Save figure
            self.canvas.figure.savefig(filepath)
