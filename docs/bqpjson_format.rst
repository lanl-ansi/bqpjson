..  _bqpjson_format:

The bqpjson Format
===================

This document describes **bqpjson**, a json-based encoding for Binary
Quadratic Programs (B-QP).  The scope of the bqpjson-format is as follows,
given:

- :math:`x` - a collection of binary variables with domains of :math:`\{-1, 1\}` or :math:`\{0, 1\}`
- :math:`L` - a collection of coefficients for each variable
- :math:`Q` - a collection of coefficients for products variables
- :math:`o` - an offset
- :math:`s` - a scaling factor

The bqpjson-format encodes the following mathematical program,

.. math::
  \min\mbox{: } & \boldsymbol s \left(\sum_{(c,i,j) \in Q} \boldsymbol c x_i x_j + \sum_{(c,i) \in L} \boldsymbol c x_i + \boldsymbol o \right) \\
  & x \in \{-1, 1\} \mbox{ or } \{0, 1\}

The goal of bqpjson is to provide a simple language-agnostic data standard for encoding such B-QPs, to assist in research and development of B-QP solution methods.

Additionally, given the significant interest in using D-Wave's QPU for
solving B-QP problems, bqpjson includes key features to assist in
encoding D-Wave inspired test cases.

Design Motivations
-------------------------

This section discusses some of the motivations for the design decisions
of bqpjson.

Spin vs Boolean Variables
~~~~~~~~~~~~~~~~~~~~~~~~~

In the operations research community, variables in B-QPs typically take
boolean values (i.e. {0, 1}). However, in the physics community the
preference is for an ising interpretation where variables take spin
values (i.e. {-1, 1}). To readily support both of these formulations,
bqpjson allows the problem variables to be defined as boolean or spin
values.

Solutions
~~~~~~~~~

A common approach when generating B-QPs is to *plant* a predefined
global optimal solution. Knowledge of these planted solutions is useful
when performing benchmarking experiments. Hence, encoding of solutions
is incorporated into the bqpjson format.

Sparse Variable Identifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a B-QP has *n* decision variables, it is often convent to number
those decision variables from 0 to n-1. Indeed the qubits in a full
yield D-Wave QPU are numbered from 0 to n-1. In practice however, D-Wave
QPUs have faults that eliminate some of the qubits. To readily support
the qubit identifiers of a D-Wave QPU, bqpjson adopts a sparse list of
variable identifiers (e.g. {0, 1, 3, 7, ..., n-3, n-1}).

Rescaling
~~~~~~~~~

Due to the physical limits of analog hardware, it is often necessary to
rescale a B-QP into the hardware's operating range. bqpjson includes a
*scaling* parameter to retain the original units of the B-QP after the
model parameters have been rescaled into the hardware's operating range.

Metadata
~~~~~~~~

When generating B-QPs it is prudent to record some data about
when and how the problem was generated. For example, when generating a 
problem on a specific D-Wave QPU, it is helpful to be able to identify 
that QPU. The bqpjson format includes a metadata block to record this 
type of information.


The JSON Document
-------------------

This section provides an informal and intuitive description of bqpjson.
Refer to ``bqpjson-schema.json`` for a formal specification.

The Document Root 
~~~~~~~~~~~~~~~~~

The root of a bqpjson document is as follows,

::

    {
      "version": <string>,
      "id": <integer>,
      "metadata": {...},
      "variable_ids": [...],
      "variable_domain": ("spin" | "boolean"),
      "scale": <float>,
      "offset": <float>,
      "linear_terms": [...],
      "quadratic_terms": [...],
      ("description": <string>,)
      ("solutions": [...])
    }

Each of the top level items is as follows:

- *version* - the version of bqpjson of this file 
- *id* - is an integer for identifying this bqp dataset 
- *metadata* - data describing how and when the problem was created 
- *variable\_ids* - a list of integers defining the valid variable identifier values 
- *variable\_domain* - indicates if the problem variables take boolean or spin values 
- *scale* - a scaling factor for the evaluation of the offset, linear and quadratic terms (typically 1.0) 
- *offset* - an offset for the evaluation of the linear and quadratic terms (typically 0.0) 
- *linear\_terms* - a list of coefficients for individual variables (a.k.a. fields) 
- *quadratic\_terms* - a list of coefficients for products variables (a.k.a. couplings) 
- *description* - an optional textual description of the bqp data 
- *solutions* - an optional list of solution objects


Linear and Quadratic Terms
~~~~~~~~~~~~~~~~~~~~~~~~~~

A linear term object has the form,

::

    {
      "id": <integer>,
      "coeff": <float>
    }

Where: 

- *id* - is the variable identifier value, it must appear in the "variable\_ids" list 
- *coeff* - this is a floating point value defining the coefficient if the given variable

Each variable should be referenced no more than once in the
"linear\_terms" list.

A quadratic term object has the form,

::

    {
      "id_tail": <integer>,
      "id_head": <integer>,
      "coeff": <float>
    }

Where: 

- *id\_tail* - is the first variable identifier value, it must appear in the "variable\_ids" list 
- *id\_head* - is the second variable identifier value, it must appear in the "variable\_ids" list 
- *coeff* - this is a floating point value defining the coefficient of the product of the given variables

Each id pair should be referenced no more than once in the
"quadratic\_terms" list and the value of *id\_tail* cannot be the same
as the value of *id\_head*. It is recommended, but not required, that
*id\_tail* be less than *id\_head*.

For example, this is **not** allowed,

::

    [
      {"id_tail": 0, "id_head": 1, "coeff": 2.4},
      {"id_tail": 0, "id_head": 1, "coeff": 1.7}
    ]

This is allowed, but not preferable,

::

    [
      {"id_tail": 0, "id_head": 1, "coeff": 2.4},
      {"id_tail": 1, "id_head": 0, "coeff": 1.7}
    ]

This is the best practice,

::

    [
      {"id_tail": 0, "id_head": 1, "coeff": 4.1}
    ]

Solutions
~~~~~~~~~

A solution object has the form,

::

    {
      "id": <integer>,
      "assignment": [...],
      ("description": <string>,)
      ("evaluation": <float>)
    }

Where: 

- *id* - is an identifier of the solution \* *assignment* - a list of assignment values for each variable defined in "variable\_ids"
- *description* - a textual description of what this solution is 
- *evaluation* - the evaluation of this solution in the given B-QP, to provided a correctness check

Each variable should be referenced exactly once in the "assignment"
list.

An assignment object has the form,

::

    {
      "id": <integer>,
      "value": <float>
    }

Where:

- *id* - is the variable identifier value, it must appear in the "variable\_ids" list 
- *value* - this is the value given to that variable

If the "variable\_domain" is "spin" the values should be either -1 or 1.
If the "variable\_domain" is "boolean" the values should be either 0 or
1.

Metadata
~~~~~~~~

A solution object has the form,

::

    {
      ("generated": <string>,)
      ("dwig_generator": <string>,)
      ("dw_url": <string>,)
      ("dw_solver_name": <string>,)
      ("dw_chip_id": <string>,)
      ("chimera_cell_size":  <integer>,)
      ("chimera_degree":  <integer>,)
      ...
    }

Where: 

- *generated* - the utc time and date that the problem was generated 
- *dwig\_generator* - the dwig algorithm used to generate the problem 
- *dw\_url* - the url of the d-wave qpu used to generate the problem 
- *dw\_solver\_name* - the name of the d-wave solver used to generate the problem 
- *dw\_chip\_id* - the chip identifier of the d-wave qpu used to generate the problem 
- *chimera\_cell\_size* - the number of variables in each chimera unit cell 
- *chimera\_degree* - the size of a square laytout of chimera unit cells

All of the metadata parameters are optional and arbitrary user defined
parameters are permitted.
