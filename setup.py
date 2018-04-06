#!/usr/bin/env python
import qurrex
from setuptools import setup
from setuptools import find_packages

packages = find_packages('.')

setup(
    name='qurrex',
    version=qurrex.__version__,
    url='https://qurrex.com',
    keywords='Qurrex, CryptoExchange, Protocol',
    description='Qurrex Exchange matching testing protocol',
    long_description='Library for testing matching engine on Qurrex',
    classifiers=[
        'Development Status :: 3 - Alpha'
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only'
    ],
    author='mf',
    author_email='mf@qurrex.com',
    license='MIT',
    packages=packages,
    include_package_data=False
)
