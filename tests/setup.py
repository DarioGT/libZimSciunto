#!/usr/bin/env python

from distutils.core import setup
from ZimBibliographer import info

setup(
    name         = 'libZimSciunto',
    version      = info.VERSION,
    url          = info.URL,
    author       = "Francois Boulogne",
    author_email = info.EMAIL,
    description  = info.SHORT_DESCRIPTION,
    packages = ['libZimSciunto'],
)
