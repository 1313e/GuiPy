# -*- coding: utf-8 -*-

"""
Base Plot Properties
====================

"""


# %% IMPORTS
# GuiPy imports
from guipy.layouts import QW_QFormLayout
from guipy.widgets import get_modified_box_signal

# All declaration
__all__ = ['BasePlotProp']


# %% CLASS DEFINITIONS
# Define BasePlotProp base class
class BasePlotProp(QW_QFormLayout):
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
    These methods return the widget name (as shown in the prop layout) and the
    widget itself.
    The widgets will also be registered as instance attributes with the same
    name as their construction method.

    The `track_values` is a bool that specifies if all widgets in this
    plot property should have their values tracked. This is *True* by default.

    """

    # Define class attributes
    NAME = ""
    DISPLAY_NAME = ""
    REQUIREMENTS = []
    WIDGET_NAMES = []
    TRACK_VALUES = True

    # Initialize this plot property
    def __init__(self, parent=None, **kwargs):
        # Call super constructor
        super().__init__(parent)

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

    # Class method for obtaining the 'track_values' of this plot property
    @classmethod
    def track_values(cls):
        return(cls.TRACK_VALUES)

    # This function sets up the plot property
    def init(self, **kwargs):
        # Save all provided kwargs as instance attributes
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Initialize empty dict of registered widgets
        self.widgets = {}

        # Loop over all items in self.widget_names
        for widget_name in self.widget_names():
            # Obtain the function to get this widget
            func = getattr(self, widget_name)

            # Call the function
            out = func()

            # Register the widget
            widget = out[-1]
            self.widgets[widget_name] = widget

            # Connect the widget to enable apply button when modified
            get_modified_box_signal(widget).connect(self.enable_apply_button)

            # Add widget as an options entry if requested
            if self.track_values():
                self.add_options_entry(widget)

            # Add widget to the layout
            self.addRow(*out)

    # Create a close method
    def close(self, *args, **kwargs):
        # Remove all widgets from options entries dict and close them
        for widget in self.widgets.values():
            # If this property uses an option entry, remove the widget
            if self.track_values():
                self.remove_options_entry(widget)

            # Close widget
            widget.close()
