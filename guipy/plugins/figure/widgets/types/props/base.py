# -*- coding: utf-8 -*-

"""
Base Plot Properties
====================

"""


# %% IMPORTS
# GuiPy imports
from guipy import layouts as GL
from guipy.widgets import get_modified_signal

# All declaration
__all__ = ['BasePlotProp']


# %% CLASS DEFINITIONS
# Define BasePlotProp base class
class BasePlotProp(GL.QFormLayout):
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
    REQUIREMENTS = ['options']
    WIDGET_NAMES = []
    TRACK_VALUES = True

    # Initialize this plot property
    def __init__(self, parent=None, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the plot property
        self.init(**kwargs)

    # This function sets up the plot property
    def init(self, **kwargs):
        # Save all provided kwargs as instance attributes
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Save specific methods of provided options
        self.get_option = self.options.get_option

        # Initialize empty dict of registered widgets
        self.widgets = {}

        # Loop over all items in self.widget_names
        for widget_name in self.WIDGET_NAMES:
            # Obtain the function to get this widget
            func = getattr(self, widget_name)

            # Call the function
            out = func()

            # Register the widget
            widget = out[-1]
            self.widgets[widget_name] = widget

            # Add widget as an options entry if requested
            if self.TRACK_VALUES:
                self.options.add_options_entry(widget)
            # Else, solely connect the modified signal to the apply button
            else:
                get_modified_signal(widget).connect(
                    self.options.enable_apply_button)

            # Add widget to the layout
            self.addRow(*out)

    # Create a close method
    def close(self, *args, **kwargs):
        # Remove all widgets from options entries dict and close them
        for widget in self.widgets.values():
            # If this property uses an option entry, remove the widget
            if self.TRACK_VALUES:
                self.options.remove_options_entry(widget)

            # Close widget
            widget.close()
