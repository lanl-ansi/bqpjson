#!/usr/bin/env python2

import sys, os, pytest, json

sys.path.append('.')
import bqpjson.bqp2mzn as bqp2mzn

from common_test import valid_bqp_files

@pytest.mark.parametrize('bqp_file', valid_bqp_files)
def test_bqp2mzn(bqp_file, capsys):

    with open(bqp_file.replace('.json', '.mzn'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        bqp2mzn.main(None, file)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())
