fcapy
=====

|Tests|
|Codecov|

Personal implementation of basic Formal Concept Analysis, not ready for productions, feedback is welcomed. 
Library is inspared by https://github.com/xflr6/concepts and it is based on https://github.com/xflr6/bitsets (probably fastest implementation of bitset in Python).

What is Formal Concept Analysis?
--------------------------------
Formal concept analysis (FCA) is a principled way of deriving a concept hierarchy or formal ontology from a collection of objects and their properties. Each concept in the hierarchy represents the objects sharing some set of properties; and each sub-concept in the hierarchy represents a subset of the objects (as well as a superset of the properties) in the concepts above it. The term was introduced by Rudolf Wille in 1980, and builds on the mathematical theory of lattices and ordered sets that was developed by Garrett Birkhoff and others in the 1930s.

https://en.wikipedia.org/wiki/Formal_concept_analysis

Links
-----
- Basic info about FCA: https://phoenix.inf.upol.cz/esf/ucebni/formal.pdf

Dependencies
------------

fcapy requires:

- Python (>= 3.4)
- bitsets

Created 2019 by Tomáš Mikula

.. |Tests| image:: https://travis-ci.org/mikulatomas/fcapy.svg?branch=master
    :target: https://travis-ci.org/mikulatomas/fcapy

.. |Codecov| image:: https://codecov.io/gh/mikulatomas/fcapy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mikulatomas/fcapy
