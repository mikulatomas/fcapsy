from setuptools import find_packages, setup

from fcapy import __version__

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(name='fcapy',
      version=__version__,
      description='Python implementation of Formal Concept Analysis',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      keywords='fca formal concept analysis',
      packages=find_packages(),
      python_requires='>=3.7',
      author='Tomas Mikula',
      author_email='mail@tomasmikula.cz',
      license='MIT',
      install_requires=['bitsets'],
      tests_require=['pytest', 'pytest-benchmark',
                     'pytest-datafiles', 'xmltodict'],
      zip_safe=False)
