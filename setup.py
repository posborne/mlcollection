#!/usr/bin/env python
from distutils.core import setup

with open('README', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(name='mlcollection',
      version='0.1',
      description='A well-designed collection of extensible machine learning algorithms',
      author='Paul Osborne',
      author_email='osbpau@gmail.com',
      requires=['numpy', 'matplotlib'],
      packages=['mlcollection'],
      long_description=LONG_DESCRIPTION,
      )
