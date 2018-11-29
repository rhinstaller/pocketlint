#!/usr/bin/python3

from setuptools import setup

setup(name='pocketlint', version='0.19',
      description='Support for running pylint against projects',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='https://github.com/rhinstaller/pocketlint',
      license='COPYING',
      install_requires=['pylint', 'polib'],
      long_description=open('README').read(),
      packages=['pocketlint', 'pocketlint.checkers'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
      ],
      )
