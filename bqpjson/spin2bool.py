#!/usr/bin/env python3

import sys, json, argparse, copy

from bqpjson.core import print_err
from bqpjson.core import validate
from bqpjson.core import swap_variable_domain


json_dumps_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}


# converts a B-QP json file from the ising space to the boolean space and vise versa.
def main(args):
    try:
        data = json.load(sys.stdin)
    except:
        print_err('unable to parse stdin as a json document')
        quit()

    output_data = swap_variable_domain(data)

    print(json.dumps(output_data, **json_dumps_kwargs))


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a B-QP json files from ising to boolean variables and back.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())