#!/usr/bin/env python

from distutils.core import setup
from libzimsciunto import info

setup(
    name         = 'libZimSciunto',
    version      = info.VERSION,
    url          = info.URL,
    author       = "Francois Boulogne",
    license      = info.LICENSE,
    author_email = info.EMAIL,
    description  = info.SHORT_DESCRIPTION,
    packages = ['libzimsciunto'],
)
