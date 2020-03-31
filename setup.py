# -*- coding: utf-8 -*-

"""
Setup file for the *GuiPy* package.

"""


# %% IMPORTS
# Built-in imports
from codecs import open
import re

# Package imports
from setuptools import find_packages, setup


# %% SETUP DEFINITION
# Get the long description from the README file
with open('README.rst', 'r') as f:
    long_description = f.read()

# Get the requirements list
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# Read the __version__.py file
with open('guipy/__version__.py', 'r') as f:
    vf = f.read()

# Obtain version from read-in __version__.py file
version = re.search(r"^_*version_* = ['\"]([^'\"]*)['\"]", vf, re.M).group(1)

# Setup function declaration
setup(name="guipy",
      version=version,
      author="Ellert van der Velden",
      author_email='ellert_vandervelden@outlook.com',
      description=("An easy plotting GUI for Python"),
      long_description=long_description,
      url='https://www.github.com/1313e/GuiPy',
      license='BSD-3',
      platforms=['Windows', 'Mac OS-X', 'Linux', 'Unix'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          ],
      keywords=('gui plotting python'),
      python_requires='>=3.6, <4',
      packages=find_packages(),
      package_dir={'guipy': "guipy"},
      # Should be 'gui_scripts', but this forces Windows to open a console
      entry_points={
          'console_scripts': [
              "guipy = guipy.app.start:main"]},
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False,
      )
