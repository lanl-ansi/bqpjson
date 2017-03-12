#!/usr/bin/env python2

import sys, os, pytest, json, io

import bqpjson

from common_test import valid_spin_bqp_files
from common_test import valid_bool_bqp_files

@pytest.mark.parametrize('bqp_file', valid_spin_bqp_files)
def test_bqp2qh_spin(bqp_file, capsys):

    with open(bqp_file.replace('.json', '.qh'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        bqpjson.bqp2qh.main(None, file)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())


@pytest.mark.parametrize('bqp_file', valid_bool_bqp_files)
def test_bqp2qh_bool(bqp_file, capsys):

    with open(bqp_file.replace('.json', '.qh'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        data_bool = json.load(file)

    #data_spin = data_bool
    data_spin = bqpjson.swap_variable_domain(data_bool)

    # python 2
    #data_stream = StringIO(json.dumps(data_bool))
    # python 3
    data_stream = io.StringIO(json.dumps(data_spin))

    bqpjson.bqp2qh.main(None, data_stream)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())
