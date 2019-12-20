# -*- coding: utf-8 -*-

"""
Base Plot Properties
====================

"""


# %% IMPORTS
# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.widgets import QW_QGroupBox

# All declaration
__all__ = ['BasePlotProp']


# %% CLASS DEFINITIONS
# Define BasePlotProp base class
class BasePlotProp(QW_QGroupBox):
    """
    Provides a base class definition that must be subclassed by all figure
    plot properties.

    Every plot property has a `name` and `display_name` associated with it;
    a list of `requirements`; and a list of all `widget_names`.

    The `name` is the name/string used internally to identify this property.

    The `display_name` is the text used in the header of the property group
    box.

    The `requirements` specify all attributes that are required by this
    property, which must be provided by the class initializing it.

    The `widget_names` are the names of the methods that must be called to
    receive the widgets for this plot property.
    These methods return the widget name (as shown in the group box) and the
    widget itself.
    The widgets will also be registered as instance attributes with the same
    name as their construction method.

    """

    # Define class attributes
    NAME = ""
    DISPLAY_NAME = ""
    REQUIREMENTS = []
    WIDGET_NAMES = []

    # Initialize this plot property
    def __init__(self, parent=None, **kwargs):
        # Call super constructor
        super().__init__(self.display_name(), parent)

        # Set up the plot property
        self.init(**kwargs)

    # Class method for obtaining the name of this plot property
    @classmethod
    def name(cls):
        return(cls.NAME)

    # Class method for obtaining the display name of this plot property
    @classmethod
    def display_name(cls):
        return(cls.DISPLAY_NAME)

    # Class method for obtaining the requirements of this plot property
    @classmethod
    def requirements(cls):
        return(cls.REQUIREMENTS)

    # Class method for obtaining the widget names of this plot property
    @classmethod
    def widget_names(cls):
        return(cls.WIDGET_NAMES)

    # This function sets up the plot property
    def init(self, **kwargs):
        # Save all provided kwargs as instance attributes
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Create a layout for this plot property
        layout = QW_QFormLayout(self)

        # Initialize empty dict of registered widgets
        self.widgets = {}

        # Loop over all items in self.widget_names
        for widget_name in self.widget_names():
            # Obtain the function to get this widget
            func = getattr(self, widget_name)

            # Call the function
            out = func()

            # Register the widget
            self.widgets[widget_name] = out[-1]

            # Add widget to the layout
            layout.addRow(*out)
