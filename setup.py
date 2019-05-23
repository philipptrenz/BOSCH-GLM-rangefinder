#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='BOSCH-GLM-rangefinder',
    version='0.0',
    author='philipptrenz',
    author_email='mail@philipptrenz.de',
    description='Remote control a BOSCH GLM 100C rangefinder via its Bluetooth serial interface.',
    url='https://github.com/philipptrenz/BOSCH-GLM-rangefinder',
    install_requires=[
        'PyBluez==0.22',
        'requests==2.22.0',
    ],
)
