============
Introduction
============

Overview
------------------------

bqpjson is a minimalist python package to support the validation and translation of binary quadratic program data in the bqpjson format.  For a description of the bqpjson format see :ref:`bqpjson_format`.  The functions provided in the :class:`bqpjson.core` module can be used to work with bqpjson data in python directly.  Stream processing command line tools, e.g. spin2bool, bqp2qh, and bqp2qubo, are also provided.  The `dwig <https://github.com/lanl-ansi/dwig>`_ project provides some examples of how bqpjson can be used.


Installation
------------------------

bqpjson is distributed via PyPI, the simplest way to install it is to run::

    pip install bqpjson


Testing
------------------------

bqpjson can be tested using setup.py by running::

    python steup.py test

