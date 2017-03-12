import json
import pytest

import bqpjson

from common_test import valid_bqp_files

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_valid(bqp_file):
    with open(bqp_file) as file:
        data = json.load(file)

    bqpjson.validate(data)
