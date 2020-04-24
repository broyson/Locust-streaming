# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='streaming_load_testing',
    version='0.1.0',
    description='Load testing for video streaming setups',
    long_description=readme,
    author='R. Ramos',
    packages=find_packages(exclude=('tests', 'docs'))
)
