# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='yatss',
    version='v0.1',
    description='Yet Another Task Scheduling Simulator',
    long_description=readme,
    author='Alexandre Amory',
    author_email='amamory@gmail.com',
    url='https://github.com//amamory-embedded//sched-learning',
    license=license,
    packages=find_packages(exclude=('docs'))
)


