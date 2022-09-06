import pathlib
from setuptools import setup, find_packages


setup(
    name="fcapsy",
    version="0.4.0",
    author="Tomáš Mikula",
    author_email="mail@tomasmikula.cz",
    description="Experimental implementations of psychological phenomena (e.g. typicality, basic level) in FCA framework.",
    keywords="fca formal concept analysis psychology cognition typicality basic-level",
    license="MIT license",
    url="https://github.com/mikulatomas/fcapsy",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["concepts@git+https://github.com/xflr6/concepts.git", "binsdpy>=0.1.1", "numpy"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
