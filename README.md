[![Build Status](https://travis-ci.com/mikulatomas/fcapsy.svg?branch=development)](https://travis-ci.com/mikulatomas/fcapsy)
[![codecov](https://codecov.io/gh/mikulatomas/fcapsy/branch/development/graph/badge.svg?token=ky2GUW51mj)](https://codecov.io/gh/mikulatomas/fcapsy)

# fcapsy

Python implementation of [Formal Concept Analysis](https://en.wikipedia.org/wiki/Formal_concept_analysis) with focus on [Cognitive Psychology](https://en.wikipedia.org/wiki/Cognitive_psychology).

Library is inspired by [concepts](https://github.com/xflr6/concepts) and it is based on [bitsets](https://github.com/xflr6/bitsets) (probably fastest implementation of bitset in Python).

⚠️ Library is mainly used for our research, not ready for production, feedback is welcomed.

![logo](https://github.com/mikulatomas/fcapsy/raw/development/logo.png)

## Basic usage
```python
import random
import pandas as pd

from fcapsy import Context, Lattice
from fcapsy.algorithms.fcbo import fcbo

df = pd.read_csv('your_favourite_boolean_dataset.csv')

# create formal context
context = Context.from_pandas(df)

# or generate random one
random_context = Context.from_random(10, 20)

# build concept lattice
lattice = Lattice.from_context(context)

# get random formal concept
concept = random.choice(lattice.concepts)

# get all upper neighbors of given concept (more general concepts)
more_general_concepts = lattice.get(concept).upper

# if u need only formal concepts, you can directly calcualte them
concepts = fcbo(context)
```

## Installation
Package is avaliable in alpha version via `pip`.

```bash
$ pip install fcapsy
```

## Used in papers

> Belohlavek, R., & Mikula, T. (2020). Typicality in Conceptual Structures Within the Framework of Formal Concept Analysis. Proceedings of CLA 2020, 33-45.
http://ceur-ws.org/Vol-2668/paper2.pdf

## Based on papers (books)
> Belohlavek, R., & Trnecka, M. (2020). Basic level of concepts in formal concept analysis 1: formalization and utilization. International Journal of General Systems, 1-18.

> Rice, M. D., & Siff, M. (2001). Clusters, concepts, and pseudometrics. Electronic Notes in Theoretical Computer Science, 40, 323-346.

> Lindig, C. (2000). Fast concept analysis. Working with Conceptual Structures-Contributions to ICCS, 2000, 152-161.

> Outrata, J., & Vychodil, V. (2012). Fast algorithm for computing fixpoints of Galois connections induced by object-attribute relational data. Information Sciences, 185(1), 114-127.

> Carpineto, C., & Romano, G. (2004). Concept data analysis: Theory and applications. John Wiley & Sons.


## What is Formal Concept Analysis?

Formal concept analysis (FCA) is a principled way of deriving a concept hierarchy or formal ontology from a collection of objects and their properties. Each concept in the hierarchy represents the objects sharing some set of properties; and each sub-concept in the hierarchy represents a subset of the objects (as well as a superset of the properties) in the concepts above it. The term was introduced by Rudolf Wille in 1980, and builds on the mathematical theory of lattices and ordered sets that was developed by Garrett Birkhoff and others in the 1930s.

https://en.wikipedia.org/wiki/Formal_concept_analysis

## Links
* Basic info about FCA: https://phoenix.inf.upol.cz/esf/ucebni/formal.pdf

## Development

Clone this repository to the folder, then:

```bash
# create virtualenv (optional)
$ mkvirtualenv fcapsy -p python3

#if is not actived (optional)
$ workon fcapsy 

$ pip install -e .

$ python setup.py test
```

## Dependencies

fcapsy requires:

* Python (>= 3.6)
* [bitsets](https://github.com/xflr6/bitsets)
