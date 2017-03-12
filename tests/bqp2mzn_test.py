import sys, os, pytest, json

import bqpjson

from common_test import valid_bqp_files
from common_test import StringIO


@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_bqp2mzn(bqp_file):

    with open(bqp_file.replace('.json', '.mzn'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        data = json.load(file)

    out = StringIO()
    bqpjson.bqpjson_to_minizinc(data, out)

    assert(out.getvalue().strip() == base.strip())
