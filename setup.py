#!/usr/bin/env python

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

__author__ = 'Tomáš Mikula'
__email__ = 'mail@tomasmikula.cz'
__version__ = '0.3.0a1'
__license__ = 'MIT license'

readme = pathlib.Path('README.md').read_text(encoding='utf-8')

history = pathlib.Path('HISTORY.md').read_text(encoding='utf-8')

setup(
    author=__author__,
    author_email=__email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Experimental implementations of psychological phenomena (e.g. typicality, basic level) in FCA framework",
    install_requires=[
        'concepts'
    ],
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=6', 'pytest-cov'],
    },
    license=__license__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    download_url='https://github.com/mikulatomas/fcapsy/archive/v0.3.0a1.tar.gz',
    include_package_data=True,
    keywords='fca formal concept analysis psychology cognition typicality basic-level',
    name='fcapsy',
    packages=find_packages(include=['fcapsy', 'fcapsy.*']),
    url='https://github.com/mikulatomas/fcapsy',
    version=__version__,
    zip_safe=False,
)
