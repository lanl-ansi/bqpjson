==========
bqpjson
==========

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

bqpjson is a minimalist python package for working with bqpjson data files, a json-based encoding of binary quadratic programs.  A detailed description of the bqpjson data format is available `here <http://bqpjson.readthedocs.io/en/latest/bqpjson_format.html>`_.  

The package can be installed via::

    pip install bqpjson


**The bqpjson toolset includes:**

- *bqpjson* - python tools for the validation and transformation of bqpjson data (`documentation <http://bqpjson.readthedocs.io/en/latest/>`_)
- *bqpjson-schema.json* - a JSON-Schema for bqpjson data files
- *spin2bool* - a command line tool for converting a bqpjson data files between the spin and boolean variable spaces
- *bqp2qh* - a command line tool for converting bqpjson data files into a qubist compatible hamiltonians
- *bqp2qubo* - a command line tool for converting bqpjson data into a qubo data
- *bqp2mzn* - a command line tool for converting bqpjson data into a minizinc model


License
------------
bqpjson is developed at Los Alamos National Laboratory and is provided under a BSD-ish license with a "modifications must be indicated" clause.  See the `LICENSE.md` file for the full text.  This package is part of the Hybrid Quantum-Classical Computing suite, known internally as LA-CC-16-032.
