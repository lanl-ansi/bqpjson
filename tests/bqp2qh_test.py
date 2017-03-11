#!/usr/bin/env python2

import sys, os, pytest, json

sys.path.append('.')
import bqpjson.bqp2qh as bqp2qh

from common_test import valid_bqp_files

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_bqp2qh(bqp_file, capsys):

    with open(bqp_file.replace('.json', '.qh'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        bqp2qh.main(None, file)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())
