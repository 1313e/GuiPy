# -*- coding: utf-8 -*-

"""
Base Formatters
===============

"""


# %% IMPORTS
# Built-in imports
import abc


# All declaration
__all__ = ['BaseFormatter']


# %% CLASS DEFINITIONS
# Define BaseFormatter abstract base class
class BaseFormatter(object, metaclass=abc.ABCMeta):
    """
    Provides an abstract base class definition that must be subclassed by all
    data table formatters.

    """

    # File type property (e.g., 'Portable Document Format')
    @property
    def type(self):
        # Return type if it is defined, or raise error if not
        if hasattr(self, 'TYPE'):
            return(self.TYPE)
        else:
            raise NotImplementedError("Class attribute 'TYPE' must be set by "
                                      "BaseFormatter subclass!")

    # File extensions property (e.g., ['.jpg', '.jpeg'])
    @property
    def exts(self):
        # Return exts if it is defined, or raise error if not
        if hasattr(self, 'EXTS'):
            return(self.EXTS)
        else:
            raise NotImplementedError("Class attribute 'EXTS' must be set by "
                                      "BaseFormatter subclass!")

    # Define exporter abstract method
    @abc.abstractmethod
    def exporter(self, data_table, filepath):
        """
        Exports the provided `data_table` to a %(ext)s-file.

        Parameters
        ----------
        data_table : :obj:`~guipy.plugins.data_table.widgets.DataTableWidget`\
            object
            The data table that must be exported.
        filepath : str
            The path to the file to be created.

        """

        # Raise NotImplementedError if only super() was called
        raise NotImplementedError("This method must be overridden in the "
                                  "BaseFormatter subclass!")

    # Define importer abstract method
    @abc.abstractmethod
    def importer(self, filepath, parent=None):
        """
        Imports a %(ext)s-file with the provided `filepath` as a
        :obj:`~pandas.DataFrame` object.

        Parameters
        ----------
        filepath : str
            The path to the %(ext)s-file.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent that will be maintaining the data.
            If *None*, no parent will be used.

        Returns
        -------
        data_table : :obj:`~pandas.DataFrame` object
            The data frame that contains all the read-in data.

        """

        # Raise NotImplementedError if only super() was called
        raise NotImplementedError("This method must be overridden in the "
                                  "BaseFormatter subclass!")
