import sys, os, pytest, json

# python 2
#from cStringIO import StringIO
# python 3
import io

import bqpjson

from common_test import valid_spin_bqp_files
from common_test import valid_bool_bqp_files
from common_test import valid_bqp_files


def check_run_func(func, input_file, base_file):
    with open(base_file, 'r') as file:
        base = file.read()

    with open(input_file, 'r') as file:
        out = io.StringIO()
        func(file, out)

    assert(out.getvalue().strip() == base.strip())


@pytest.mark.parametrize('bqp_file', valid_spin_bqp_files)
def test_run_bqp2qh_spin(bqp_file):
    check_run_func(bqpjson.cli.run_bqp2qh, bqp_file, bqp_file.replace('.json', '.qh'))

@pytest.mark.parametrize('bqp_file', valid_bool_bqp_files)
def test_run_bqp2qubo_bool(bqp_file):
    check_run_func(bqpjson.cli.run_bqp2qubo, bqp_file, bqp_file.replace('.json', '.qubo'))

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_run_bqp2mzn(bqp_file):
    check_run_func(bqpjson.cli.run_bqp2mzn, bqp_file, bqp_file.replace('.json', '.mzn'))

@pytest.mark.parametrize('bqp_file', valid_spin_bqp_files)
def test_run_spin2bool_spin(bqp_file):
    with open(bqp_file.replace('.json', '.qubo'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        out_bool = io.StringIO()
        bqpjson.cli.run_spin2bool(file, out_bool)

    out = io.StringIO()
    bqpjson.cli.run_bqp2qubo(io.StringIO(out_bool.getvalue()), out)

    assert(out.getvalue().strip() == base.strip())

