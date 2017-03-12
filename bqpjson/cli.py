#!/usr/bin/env python3
from __future__ import print_function

import sys, json, argparse

from bqpjson.core import print_err
from bqpjson import validate
from bqpjson import swap_variable_domain
from bqpjson import bqpjson_to_qubist
from bqpjson import bqpjson_to_qubo
from bqpjson import bqpjson_to_minizinc

_json_pretty_print_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}

def load_data(data_steam):
    try:
        data = json.load(data_steam)
    except:
        print_err('unable to parse stdin as a json document')
        quit()
    return data


# converts a bqp-json file to a qubist hamiltonian
def bqp2qh():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    args = parser.parse_args()
    run_bqp2qh()

def run_bqp2qh(in_stream=sys.stdin, out_stream=sys.stdout):
    data = load_data(data_steam=in_stream)
    bqpjson_to_qubist(data=data, out_stream=out_stream)


# converts a bqp-json file to a qubo data file
def bqp2qubo():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubo format.  The default input is stdin and the default output is stdout.')
    args = parser.parse_args()
    run_bqp2qubo()

def run_bqp2qubo(in_stream=sys.stdin, out_stream=sys.stdout):
    data = load_data(data_steam=in_stream)
    bqpjson_to_qubo(data=data, out_stream=out_stream)


# converts a bqp-json file to a qubist hamiltonian
def run_bqp2mzn(in_stream=sys.stdin, out_stream=sys.stdout):
    data = load_data(data_steam=in_stream)
    bqpjson_to_minizinc(data=data, out_stream=out_stream)

def bqp2mzn():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    args = parser.parse_args()
    run_bqp2mzn()


# converts a B-QP json file from the ising space to the boolean space and vise versa.
def run_spin2bool(in_stream=sys.stdin, out_stream=sys.stdout, pretty_print=False):
    data = load_data(data_steam=in_stream)
    output_data = swap_variable_domain(data)
    if pretty_print:
        print(json.dumps(output_data, **_json_pretty_print_kwargs), file=out_stream)
    else:
        print(json.dumps(output_data, sort_keys=True), file=out_stream)

def spin2bool():
    parser = argparse.ArgumentParser(description='a command line tool for converting a B-QP json files from ising to boolean variables and back.  The default input is stdin and the default output is stdout.')
    parser.add_argument('-pp', '--pretty-print', help='pretty print json output', action='store_true', default=False)
    args = parser.parse_args()
    run_spin2bool(pretty_print=args.pretty_print)

