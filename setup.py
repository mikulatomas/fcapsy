import pathlib
from setuptools import setup, find_packages
from fcapsy import __version__, __author__, __email__, __license__


setup(
    name="fcapsy",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Experimental implementations of psychological phenomena (e.g. typicality, basic level) in FCA framework.",
    keywords="fca formal concept analysis psychology cognition typicality basic-level",
    license=__license__,
    url="https://github.com/mikulatomas/fcapsy",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["concepts>=0.9.2", "binsdpy>=0.1.1"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Science/Research",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
