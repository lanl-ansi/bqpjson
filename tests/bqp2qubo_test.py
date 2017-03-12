import sys, os, pytest, json

# python 2
#from cStringIO import StringIO
# python 3
import io

import bqpjson

from common_test import valid_spin_bqp_files
from common_test import valid_bool_bqp_files

@pytest.mark.parametrize('bqp_file', valid_spin_bqp_files)
def test_bqp2qh_spin(bqp_file, capsys):
    with open(bqp_file.replace('.json', '.qubo'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        data_spin = json.load(file)

    data_bool = bqpjson.swap_variable_domain(data_spin)

    # python 2
    #data_stream = StringIO(json.dumps(data_bool))
    # python 3
    #data_stream = io.StringIO(json.dumps(data_bool))

    #bqpjson.bqp2qubo.run(None, data_stream)
    bqpjson.bqpjson_to_qubo(data_bool, sys.stdout)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())


@pytest.mark.parametrize('bqp_file', valid_bool_bqp_files)
def test_bqp2qh_bool(bqp_file, capsys):
    with open(bqp_file.replace('.json', '.qubo'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        data = json.load(file)

    bqpjson.bqpjson_to_qubo(data, sys.stdout)


    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())