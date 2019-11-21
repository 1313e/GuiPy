# -*- coding: utf-8 -*-

"""
Config Core
===========
Provides a collection of core definitions that are required for all
configurations in *GuiPy*.

"""


# %% IMPORTS
# All declaration
__all__ = ['ntr', 'tr']


# %% FUNCTION DEFINITIONS
# This function marks a string to not be automatically translated
def ntr(text):
    """
    Marks the provided `text` to not be automatically translated if it would be
    passed to the :func:`~tr` function.

    Parameters
    ----------
    text : str
        The text string that should not be automatically translated by
        :func:`~tr`.

    Returns
    -------
    marked_text : str
        The text string `text`, but marked for no auto-translation.

    """

    # For now, just return the text again
    return(text)


# This function automatically translates a text string that is given to it
def tr(text):
    """
    Translates the provided `text` from English to the current language
    setting.

    If no translation exists for `text`, it is returned instead.

    Parameters
    ----------
    text : str
        The text string that needs to be translated to the current language set
        for *GuiPy*.

    Returns
    -------
    translation : str
        The translation of `text` to the current language. If no translation
        exists, `text` is returned instead.

    """

    # For now, just return the text again
    return(text)
