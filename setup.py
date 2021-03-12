#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

__author__ = 'Tomáš Mikula, Roman Vyjídáček'
__email__ = 'mail@tomasmikula.cz, r.vyjidacek@gmail.com'
__version__ = '0.1.0'
__license__ = 'MIT license'

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

# Requirements for end-user
requirements = [
    'bitsets>=0.7']

# Requirements for test
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', 'pandas']

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
    description="Formal Concept Analysis implementation with focus on Cognitive Psychology",
    install_requires=requirements,
    license=__license__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='fca formal concept analysis psychology cognition typicality basic-level',
    name='fcapsy',
    packages=find_packages(include=['fcapsy', 'fcapsy.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mikulatomas/fcapsy',
    version=__version__,
    zip_safe=False,
)
