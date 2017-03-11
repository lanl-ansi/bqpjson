import os, sys, json
import jsonschema

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bqpjson-schema.json')) as file:
    _qbpjson_schema = json.load(file)

_bqpjson_versions = ['0.1.0']
_bqpjson_version_latest = _bqpjson_versions[-1]

def validate(data):
    jsonschema.validate(data, _qbpjson_schema)

    assert(data['scale'] >= 0.0)

    var_ids = {i for i in data['variable_ids']}
    for lt in data['linear_terms']:
        assert(lt['id'] in var_ids)

    for qt in data['quadratic_terms']:
        assert(qt['id_tail'] in var_ids)
        assert(qt['id_head'] in var_ids)
        assert(qt['id_tail'] != qt['id_head'])
        if qt['id_tail'] > qt['id_head']:
            # TODO warn
            pass

    if 'solutions' in data:
        for solution in data['solutions']:
            sol_ids = {}
            for assign in solution['assignment']:
                assert(assign['id'] in var_ids)
                assert(not assign['id'] in sol_ids)
                sol_ids.add(assign['id'])
                if data['variable_domain'] == 'spin':
                    assert(assign['value'] == -1 or assign['value'] == 1)
                if data['variable_domain'] == 'boolean':
                    assert(assign['value'] == 0 or assign['value'] == 1)
            assert(len(sol_ids) == len(var_ids))


