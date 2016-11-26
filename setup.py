# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='HTTP Log Monitor',
    version='1.0.0',
    description='Simple HTTP Log Monitor (Datadogs homework assignement)',
    long_description=readme,
    author='Jeremy Guiselin',
    author_email='jeremy.guiselin@outlook.com',
    url='https://github.com/Jrmyy/http-log-monitor',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
