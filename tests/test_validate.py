import json
import os

import bqpjson

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def test_000():
    with open(os.path.join(data_dir, '000.json')) as file:
        data = json.load(file)

    bqpjson.validate(data)


def test_001():
    with open(os.path.join(data_dir, '001.json')) as file:
        data = json.load(file)

    bqpjson.validate(data)


def test_002():
    with open(os.path.join(data_dir, '002.json')) as file:
        data = json.load(file)

    bqpjson.validate(data)
