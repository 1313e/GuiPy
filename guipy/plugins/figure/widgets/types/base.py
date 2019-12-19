# -*- coding: utf-8 -*-

"""
Base Plot Types
===============

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC

# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.plugins.figure.widgets.types.props import PLOT_PROPS
from guipy.widgets import QW_QWidget, get_box_value, set_box_value

# All declaration
__all__ = ['BasePlotType']


# %% CLASS DEFINITIONS
# Define BasePlotType base class
class BasePlotType(QW_QWidget):
    """
    Provides a base class definition that must be subclassed by all figure plot
    types.

    Every plot type has a `name` associated with it; and a list of all
    `prop_names`.

    The `name` is the name/string used internally to identify this property.

    The `prop_names` are the names of the plot properties that this plot type
    uses. The 'Data' property is used by default and does not need to be
    provided.

    """

    # Define class attributes
    NAME = ""
    PROP_NAMES = []

    # Signals
    labelChanged = QC.Signal(str)

    # Initialize this plot type
    def __init__(self, name, toolbar, parent=None, *args, **kwargs):
        # Save provided FigureToolbar object
        self.toolbar = toolbar
        self.data_table_plugin = toolbar.data_table_plugin
        self.figure = toolbar.canvas.figure
        self.axis = self.figure.gca()

        # Call super constructor
        super().__init__(parent)

        # Set up the plot entry box
        self.init(name, *args, **kwargs)

    # Class method for obtaining the name of this plot type
    @classmethod
    def name(cls):
        return(cls.NAME)

    # Class method for obtaining the property names of this plot type
    @classmethod
    def prop_names(cls):
        return(cls.PROP_NAMES)

    # This function sets up the plot type
    def init(self, name):
        # Create layout for this line plot
        self.create_type_layout()

        # Connect signals
        self.labelChanged.connect(self.set_plot_label)

        # Save that currently no line exists
        self.plot = None
        set_box_value(self.data_label_box, name)

    # This function creates the type layout
    def create_type_layout(self):
        # Create layout for this plot type
        layout = QW_QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Loop over all required plot props
        for prop_name in self.prop_names():
            # Obtain the PlotProp class associated with this property
            plot_prop_class = PLOT_PROPS[prop_name]

            # Obtain a dictionary with all requirements of this property
            prop_kwargs = {req: getattr(self, req)
                           for req in plot_prop_class.requirements()}

            # Initialize the property and add to layout
            prop_group = plot_prop_class(**prop_kwargs)
            layout.addRow(prop_group)

            # Register all widgets in this property as instance attributes
            for widget_name, widget in prop_group.widgets.items():
                setattr(self, widget_name, widget)

    # Define draw_plot method
    @QC.Slot()
    def draw_plot(self):
        """
        Draws the current plot.

        """

        raise NotImplementedError(self.__class__)

    # Define update_plot method
    @QC.Slot()
    def update_plot(self):
        """
        Updates the current plot.

        """

        raise NotImplementedError(self.__class__)

    # Define set_plot_label method
    @QC.Slot(str)
    def set_plot_label(self, label):
        """
        Sets the label of the current plot.

        """

        raise NotImplementedError(self.__class__)
