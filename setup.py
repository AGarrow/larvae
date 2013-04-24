#!/usr/bin/env python
# Copyright (c) Sunlight Labs, 2013 under the terms and conditions
# of the LICENSE file.

from larvae import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    name       = __appname__,
    version    = __version__,
    packages   = ['larvae'],

    author       = "Paul Tagliamonte",
    author_email = "paultag@sunlightfoundation.com",

    long_description = long_description,
    description      = 'Validation layer for open civic data objects.',
    license          = "BSD-3",

    platforms        = ['any'],
    install_requires = ['validictory'],
)
