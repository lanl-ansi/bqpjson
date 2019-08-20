
__version__ = '0.5.3'

from bqpjson.core import (
    validate, evaluate, swap_variable_domain, spin_to_bool, bool_to_spin,
    bqpjson_to_qubist, bqpjson_to_qubo, bqpjson_to_minizinc, bqpjson_to_hfs
)

# needed for testing, not deployment
from bqpjson import cli
