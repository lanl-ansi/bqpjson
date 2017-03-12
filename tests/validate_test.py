import json
import pytest

import bqpjson

from common_test import valid_bqp_files

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_valid(bqp_file):
    with open(bqp_file) as file:
        data = json.load(file)
    if 'solutions' in data:
        for solution in data['solutions']:
            assignment = {item['id']:item['value'] for item in solution['assignment']}
            val = bqpjson.evaluate(data, assignment)
            if 'evaluation' in solution:
                assert(val == solution['evaluation'])
