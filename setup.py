#!/usr/bin/python3

from distutils.core import setup

setup(name='pocketlint', version='1',
      description='Support for running pylint against projects',
      author='Chris Lumens', author_email='clumens@redhat.com',
      requires=['pylint'],
      packages=['pocketlint', 'pocketlint.checkers'])
