#!/usr/bin/env python
# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

from popolo import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    name       = __appname__,
    version    = __version__,
    packages   = ['popolo'],

    author       = "Paul Tagliamonte",
    author_email = "paultag@sunlightfoundation.com",

    long_description = long_description,
    description      = 'Validation layer for Popolo objects.',
    license          = "BSD-3",

    platforms        = ['any']
)
