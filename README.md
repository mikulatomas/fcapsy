# fcapy

Python implementation of Formal Concept Analysis.

Library is inspired by https://github.com/xflr6/concepts and it is based on https://github.com/xflr6/bitsets (probably fastest implementation of bitset in Python).

⚠️ Library is mainly used for our research, not ready for production, feedback is welcomed.

## What is Formal Concept Analysis?

Formal concept analysis (FCA) is a principled way of deriving a concept hierarchy or formal ontology from a collection of objects and their properties. Each concept in the hierarchy represents the objects sharing some set of properties; and each sub-concept in the hierarchy represents a subset of the objects (as well as a superset of the properties) in the concepts above it. The term was introduced by Rudolf Wille in 1980, and builds on the mathematical theory of lattices and ordered sets that was developed by Garrett Birkhoff and others in the 1930s.

https://en.wikipedia.org/wiki/Formal_concept_analysis

## Links
* Basic info about FCA: https://phoenix.inf.upol.cz/esf/ucebni/formal.pdf

## Used in papers

> Belohlavek, R., & Mikula, T. (2020). Typicality in Conceptual Structures Within the Framework of Formal Concept Analysis. Proceedings of CLA 2020, 33-45.


## Development

Clone this repository to the folder, then:

```bash
# create virtualenv (optional)
$ mkvirtualenv fcapy -p python3

#if is not actived (optional)
$ workon fcapy 

$ pip install -e .

$ python setup.py test
```

## Dependencies

fcapy requires:

* Python (>= 3.6)
* bitsets