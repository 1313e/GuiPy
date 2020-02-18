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
from guipy.widgets import QW_QGroupBox, QW_QWidget

# All declaration
__all__ = ['BasePlotType']


# %% CLASS DEFINITIONS
# Define BasePlotType base class
class BasePlotType(QW_QWidget):
    """
    Provides a base class definition that must be subclassed by all figure plot
    types.

    Every plot type has a `name` and `prefix` associated with it; can be used
    for a specific `axis_type`; and a list of all `prop_names`.

    The `name` is the name/string used internally to identify this property.

    The `prefix` is the string used as a prefix for texts/names that relate to
    this plot type.

    The `display_name` is the text used in the types combobox.

    The `prop_names` are the names of the plot properties that this plot type
    uses. The 'Data' property is used by default and does not need to be
    provided.

    """

    # Define class attributes
    NAME = ""
    PREFIX = ""
    AXIS_TYPE = ""
    PROP_NAMES = []

    # Signals
    dataLabelChanged = QC.Signal(str)

    # Initialize this plot type
    def __init__(self, toolbar, parent=None, *args, **kwargs):
        # Save provided FigureToolbar object
        self.toolbar = toolbar
        self.options = toolbar.options_dialog
        self.data_table_plugin = toolbar.data_table_plugin
        self.figure = toolbar.canvas.figure
        self.axis = self.figure.gca()

        # Save the option getter
        self.get_option = self.options.get_option

        # Call super constructor
        super().__init__(parent)

        # Set up the plot entry box
        self.init(*args, **kwargs)

    # This function sets up the plot type
    def init(self):
        # Create layout for this line plot
        self.create_type_layout()

        # Connect signals
        self.dataLabelChanged.connect(self.set_plot_label)

        # Save that currently no line exists
        self.plot = None

        # Attempt to update the plot to check if that does not raise errors
        self.update_plot()

    # This function creates the type layout
    def create_type_layout(self):
        # Create empty list of properties
        self.props = []

        # Create layout for this plot type
        layout = QW_QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Loop over all required plot props
        for prop_name in self.PROP_NAMES:
            # Obtain the PlotProp class associated with this property
            plot_prop_class = PLOT_PROPS[prop_name]

            # Create a dictionary with all requirements of this property
            prop_kwargs = {req: getattr(self, req)
                           for req in plot_prop_class.REQUIREMENTS}

            # Initialize the property and add to layout
            # TODO: Create a collapsable QGroupBox widget
            prop_layout = plot_prop_class(**prop_kwargs)
            prop_group = QW_QGroupBox(prop_layout.DISPLAY_NAME)
            prop_group.setLayout(prop_layout)
            layout.addRow(prop_group)
            self.props.append(prop_layout)

            # Register all widgets in this property as instance attributes
            for widget_name, widget in prop_layout.widgets.items():
                setattr(self, widget_name, widget)

    # Define update_plot method
    @QC.Slot()
    def update_plot(self):
        """
        Draws and updates the current plot. This function must implement a
        check for whether updating is necessary/required.

        """

        raise NotImplementedError(self.__class__)

    # Define remove_plot method
    @QC.Slot()
    def remove_plot(self):
        """
        Removes the current plot.

        """

        raise NotImplementedError(self.__class__)

    # Define set_plot_label method
    @QC.Slot(str)
    def set_plot_label(self, label):
        """
        Sets the label of the current plot.

        """

        raise NotImplementedError(self.__class__)

    # Override closeEvent to remove all plots and props
    def closeEvent(self, *args, **kwargs):
        # Remove the plots from the figure if they exist
        if self.plot is not None:
            self.remove_plot()

        # Close all props
        for prop in self.props:
            prop.close()

        # Call super event
        super().closeEvent(*args, **kwargs)
