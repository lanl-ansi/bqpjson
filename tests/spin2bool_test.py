import sys, os, pytest, json, math

import bqpjson

from common_test import valid_bqp_files


@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_spin2bool(bqp_file):
    with open(bqp_file) as file:
        data_0 = json.load(file)

    data_1 = bqpjson.swap_variable_domain(data_0)
    data_2 = bqpjson.swap_variable_domain(data_1)

    # These tests are required to get around numerical precision issues in floating point arithmetic
    assert(math.isclose(data_0['offset'], data_2['offset']))

    for i in range(len(data_0['linear_terms'])):
        assert(math.isclose(data_0['linear_terms'][i]['coeff'], data_2['linear_terms'][i]['coeff']))

    for i in range(len(data_0['quadratic_terms'])):
        assert(math.isclose(data_0['quadratic_terms'][i]['coeff'], data_2['quadratic_terms'][i]['coeff']))

    for key in ['offset', 'linear_terms', 'quadratic_terms']:
        for data in [data_0, data_2]:
            del data[key]

    assert(data_0 == data_2)
