import json
import pytest
import math

import bqpjson

from common_test import valid_bqp_files

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_valid(bqp_file):
    with open(bqp_file) as file:
        data = json.load(file)

    values = bqpjson.evaluate(data)

    if 'solutions' in data:
        for i, solution in enumerate(data['solutions']):
            assert(math.isclose(values[i], solution['evaluation']))
    else:
        assert(len(values) == 0)

