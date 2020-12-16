# -*- coding: utf-8 -*-

"""
General Config
==============

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.config import BaseConfigPage
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['GeneralConfigPage']


# %% HELPER DEFINITIONS
# Define special ComboBox for setting country and language values
class LocaleComboBox(GW.BaseBox):
    # Signals
    modified = QC.Signal([], [int])

    # Override constructor
    def __init__(self, locale_type, parent=None):
        # Handle provided locale_type
        if(locale_type == 'country'):
            self.f_ToString = QC.QLocale.countryToString
        else:
            self.f_ToString = QC.QLocale.languageToString

        # Call super constructor
        super().__init__(parent)

        # Create the combobox
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[int])

    # This function creates the combobox
    def init(self):
        # Create layout
        layout = GL.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create combobox
        combobox = GW.QComboBox()
        layout.addWidget(combobox)
        self.combobox = combobox

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit current value
        self.modified[int].emit(get_box_value(self))

    # Override addItems to store additional item information
    def addItems(self, items):
        # Loop over all items and add them to the combobox
        for i, item in enumerate(items):
            self.combobox.addItem(self.f_ToString(item))
            self.combobox.setItemData(i, item)

    # This function retrieves a value of this combobox
    def get_box_value(self, *value_sig):
        # Obtain the current index of this combobox
        index = get_box_value(self.combobox, int)

        # Obtain the corresponding user data
        value = self.combobox.itemData(index)

        # Return value
        return(value)

    # This function sets the value of this combobox
    def set_box_value(self, value, *value_sig):
        # Convert provided value to appropriate string
        string = self.f_ToString(value)

        # Set value of this combobox
        set_box_value(self.combobox, string)


# %% CLASS DEFINITIONS
# Define config page for setting the general config
class GeneralConfigPage(BaseConfigPage):
    # Define class attributes
    NAME = 'General'

    # This function sets up the General config page
    def init(self):
        # Create layout
        layout = GL.QVBoxLayout(self)

        # Create 'General' group box
        general_group = GW.QGroupBox("General")
        layout.addWidget(general_group)
        general_layout = GL.QFormLayout(general_group)

        # Add combobox for language-settings
        language_box = LocaleComboBox('language')
        language_box.addItems(list({QC.QLocale.system().language(),
                                    QC.QLocale.English}))
        language_box.setToolTip("Set the language used for representing "
                                "strings and values.")
        self.add_config_entry('language', language_box, True)
        general_layout.addRow("Language", language_box)

    # This function parses and processes a config section, and returns it
    def decode_config(self, section_dict):
        # Initialize empty dict of parsed config values
        config_dict = sdict()

        # Decode all values in section_dict
        for key, value in section_dict.items():
            # Add all values to config dict using literal_eval
            config_dict[key] = literal_eval(value)

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        # Create default dict
        default_dict = sdict({
            'language': QC.QLocale.system().language()})

        # Return default_dict
        return(default_dict)

    # This function returns its config section, as required by config parser
    def encode_config(self, config_dict):
        # Initialize empty dict of section config values
        section_dict = sdict()

        # Loop over all arguments in config and encode them in
        for key, value in config_dict.items():
            section_dict[key] = '{!r}'.format(value)

        # Return section_dict
        return(section_dict)

    # This function applies the currently stored config
    def apply_config(self, config_dict):
        # Create new QLocale
        locale = QC.QLocale(config_dict['language'])

        # Set this as the new default
        QC.QLocale.setDefault(locale)
