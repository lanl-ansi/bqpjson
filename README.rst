==========
bqpjson
==========

**release:**

.. image:: https://badge.fury.io/py/bqpjson.svg
    :target: https://badge.fury.io/py/bqpjson

.. image:: https://readthedocs.org/projects/bqpjson/badge/?version=stable
  :target: http://bqpjson.readthedocs.io/en/stable/?badge=stable
  :alt: Documentation Status


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
- *bqp2qh* - a command line tool for converting bqpjson data files into qubist compatible hamiltonians
- *bqp2qubo* - a command line tool for converting bqpjson data into qubo data
- *bqp2mzn* - a command line tool for converting bqpjson data into a minizinc model
- *bqp2hfs* - a command line tool for converting bqpjson data into hfs data


**An example of bqpjson data**::

    {
      "description":"a simple model",
      "id": 0,
      "linear_terms": [
        {"coeff":  1.3, "id": 2},
        {"coeff": -0.7, "id": 6}
      ],
      "metadata": {},
      "offset": 0.0,
      "quadratic_terms": [
        {"coeff": -0.2, "id_head": 4, "id_tail": 2},
        {"coeff":  1.5, "id_head": 6, "id_tail": 2}
      ],
      "scale": 1.0,
      "variable_domain": "spin",
      "variable_ids": [2,4,6],
      "version": "1.0.0"
    }


License
------------
bqpjson is developed at Los Alamos National Laboratory and is provided under a BSD-ish license with a "modifications must be indicated" clause.  See the `LICENSE.md` file for the full text.  This package is part of the Hybrid Quantum-Classical Computing suite, known internally as LA-CC-16-032.


Changelog
------------

**staged**

- improved bqp2hfs robustness to coefficient precision issues
- dropped support for python 2.7 and 3.4


**v0.5.1**

- added support for translation to the HFS data format


**v0.5.0**

- initial release

