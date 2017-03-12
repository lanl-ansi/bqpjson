==========
bqpjson
==========
Utilities for working with bqpjson data

**dev status:**

.. image:: https://travis-ci.org/lanl-ansi/bqpjson.svg?branch=master
  :target: https://travis-ci.org/lanl-ansi/bqpjson
  :alt: Build Report
.. image:: https://codecov.io/gh/lanl-ansi/bqpjson/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/lanl-ansi/bqpjson
  :alt: Coverage Report
.. image:: https://readthedocs.org/projects/bqpjson/badge/?version=latest
  :target: http://bqpjson.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


The bqpjson toolset includes:

- *bqpjson* - a python library for the validation and transformation of bqpjson data
- *bqpjson-schema.json* - a JSON-Schema for bqpjson data files
- *spin2bool* - a command line tool for converting a bqpjson data files between the spin and boolean variable spaces
- *bqp2qh* - a command line tool for converting bqpjson data files into a qubist compatible hamiltonians
- *bqp2qubo* - a command line tool for converting bqp-json data into a qubo data
- *bqp2mzn* - a command line tool for converting bqp-json data into a minizinc model


License
------------
bqpjson was developed at Los Alamos National Laboratory and is provided under a BSD-ish license with a "modifications must be indicated" clause.  See the `LICENSE.md` file for the full text.  This package is part of the Hybrid Quantum-Classical Computing suite, known internally as LA-CC-16-032.
