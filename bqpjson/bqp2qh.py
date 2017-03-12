#!/usr/bin/env python3

import sys, json, argparse

from bqpjson.core import print_err
from bqpjson import validate
from bqpjson import bqpjson_to_qubist

# converts a bqp-json file to a qubist hamiltonian
def main(args, data_stream):
    try:
        data = json.load(data_stream)
    except:
        print_err('unable to parse stdin as a json document')
        quit()

    bqpjson_to_qubist(data=data, out_stream=sys.stdout)


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args(), sys.stdin)
