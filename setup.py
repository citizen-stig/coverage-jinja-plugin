#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from distutils.core import setup

setup(
    name='jinja_coverage',
    version='0.1',
    description='Jinja2 coverage.py plugin',
    author='Nikolay Golub',
    author_email='nikolay.v.golub@gmail.com',
    url='',
    packages=['jinja_coverage'],
    install_requires=[
        'Jinja2 >= 2.8',
        'coverage >= 4.1b2',
    ],
)
