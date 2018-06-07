#!/usr/bin/python3

from distutils.core import setup

setup(name='pocketlint', version='0.16',
      description='Support for running pylint against projects',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='https://github.com/rhinstaller/pocketlint',
      requires=['pylint'],
      packages=['pocketlint', 'pocketlint.checkers'])
