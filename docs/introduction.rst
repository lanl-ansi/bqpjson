============
Introduction
============

Overview
------------------------

bqpjson is a minimalist python package to support the validation and translation of binary quadratic program data in the bqpjson format.  For a description of the bqpjson format see :ref:`bqpjson_format`.  The functions provided in the :class:`bqpjson.core` module can be used to work with bqpjson data in python directly, however stream processing command line tools, e.g. spin2bool, bqp2qh,  bqp2qubo, are also provided.


Installation
------------------------

bqpjson is not currently available on pypi.  The simplest installation is to checkout the repository and run::

    pip install .

