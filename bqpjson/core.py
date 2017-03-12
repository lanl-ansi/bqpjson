import os, sys, json, copy

from functools import partial

import jsonschema

# prints a line to standard error
print_err = partial(print, file=sys.stderr)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bqpjson-schema.json')) as file:
    _qbpjson_schema = json.load(file)

_bqpjson_versions = ['0.1.0']
_bqpjson_version_latest = _bqpjson_versions[-1]


def validate(data):
    jsonschema.validate(data, _qbpjson_schema)

    assert(data['scale'] >= 0.0)

    var_ids = {i for i in data['variable_ids']}
    lt_vars = set([])
    for lt in data['linear_terms']:
        assert(lt['id'] in var_ids)
        assert(lt['id'] not in lt_vars)
        lt_vars.add(lt['id'])

    qt_var_pairs = set([])
    for qt in data['quadratic_terms']:
        assert(qt['id_tail'] in var_ids)
        assert(qt['id_head'] in var_ids)
        assert(qt['id_tail'] != qt['id_head'])
        if qt['id_tail'] > qt['id_head']:
            # TODO warn
            pass
        pair = (qt['id_tail'], qt['id_head'])
        assert(pair not in qt_var_pairs)
        qt_var_pairs.add(pair)

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


def swap_variable_domain(data):
    validate(data)
    if data['variable_domain'] == 'spin':
        output_data = spin_to_bool(data)
    else:
        output_data = bool_to_spin(data)
    return output_data


def spin_to_bool(ising_data):
    validate(ising_data)
    assert(ising_data['variable_domain'] == 'spin')

    offset = ising_data['offset']
    coefficients = {}

    for v_id in ising_data['variable_ids']:
        coefficients[(v_id, v_id)] = 0.0

    for linear_term in ising_data['linear_terms']:
        v_id = linear_term['id']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = 2.0*coeff
        offset += -coeff

    for quadratic_term in ising_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        assert(v_id1 != v_id2)
        # if v_id1 > v_id2:
        #     v_id1 = quadratic_term['id_head']
        #     v_id2 = quadratic_term['id_tail']
        coeff = quadratic_term['coeff']
        assert(coeff != 0.0)

        if not (v_id1, v_id2) in coefficients:
            coefficients[(v_id1, v_id2)] = 0.0

        coefficients[(v_id1, v_id2)] = coefficients[(v_id1, v_id2)] + 4.0*coeff
        coefficients[(v_id1, v_id1)] = coefficients[(v_id1, v_id1)] - 2.0*coeff
        coefficients[(v_id2, v_id2)] = coefficients[(v_id2, v_id2)] - 2.0*coeff
        offset += coeff

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'id':i, 'coeff':v})
            else:
                quadratic_terms.append({'id_tail':i, 'id_head':j, 'coeff':v})

    bool_data = copy.deepcopy(ising_data)
    bool_data['variable_domain'] = 'boolean'
    bool_data['offset'] = offset
    bool_data['linear_terms'] = linear_terms
    bool_data['quadratic_terms'] = quadratic_terms

    if 'solutions' in bool_data:
        for solution in bool_data['solutions']:
            for assign in solution['assignment']:
                if assign['value'] == -1:
                    assign['value'] = 0

    return bool_data


def bool_to_spin(bool_data):
    validate(bool_data)
    assert(bool_data['variable_domain'] == 'boolean')

    offset = bool_data['offset']
    coefficients = {}

    for v_id in bool_data['variable_ids']:
        coefficients[(v_id, v_id)] = 0.0

    for linear_term in bool_data['linear_terms']:
        v_id = linear_term['id']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = coeff/2.0
        offset += linear_term['coeff']/2.0

    for quadratic_term in bool_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        assert(v_id1 != v_id2)
        # if v_id1 > v_id2:
        #     v_id1 = quadratic_term['id_head']
        #     v_id2 = quadratic_term['id_tail']
        coeff = quadratic_term['coeff']
        assert(coeff != 0.0)

        if not (v_id1, v_id2) in coefficients:
            coefficients[(v_id1, v_id2)] = 0.0

        coefficients[(v_id1, v_id2)] = coefficients[(v_id1, v_id2)] + coeff/4.0
        coefficients[(v_id1, v_id1)] = coefficients[(v_id1, v_id1)] + coeff/4.0
        coefficients[(v_id2, v_id2)] = coefficients[(v_id2, v_id2)] + coeff/4.0
        offset += coeff/4.0

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'id':i, 'coeff':v})
            else:
                quadratic_terms.append({'id_tail':i, 'id_head':j, 'coeff':v})

    ising_data = copy.deepcopy(bool_data)
    ising_data['variable_domain'] = 'spin'
    ising_data['offset'] = offset
    ising_data['linear_terms'] = linear_terms
    ising_data['quadratic_terms'] = quadratic_terms

    if 'solutions' in ising_data:
        for solution in ising_data['solutions']:
            for assign in solution['assignment']:
                if assign['value'] == 0:
                    assign['value'] = -1

    return ising_data


def bqpjson_to_qubist(data, out_stream):
    validate(data)

    print2out = partial(print, file=out_stream)

    if data['variable_domain'] == 'boolean':
        print_err('Error: unable to generate qubist hamiltonian from stdin, only spin domains are supported by qubist')
        quit()

    quadratic_terms = {}
    for qt in data['quadratic_terms']:
        i,j = qt['id_tail'],qt['id_head']
        if i > j:
            i,j = qt['id_head'],qt['id_tail']
        pair = (i,j)
        if pair not in quadratic_terms:
            quadratic_terms[pair] = qt['coeff']
        else:
            print_err('Warning: merging multiple values quadratic terms between {},{}'.format(i,j))
            quadratic_terms[pair] = quadratic_terms[pair] + qt['coeff']

    sites = max(data['variable_ids'])+1 if len(data['variable_ids']) > 0 else 0
    lines = len(data['linear_terms']) + len(data['quadratic_terms'])

    print2out('{} {}'.format(sites, lines))
    for lt in data['linear_terms']:
        print2out('{} {} {}'.format(lt['id'], lt['id'], lt['coeff']))
    for (i,j) in sorted(quadratic_terms.keys()):
        v = quadratic_terms[(i,j)]
        print2out('{} {} {}'.format(i, j, v))


def bqpjson_to_qubo(data, out_stream):
    validate(data)

    print2out = partial(print, file=out_stream)

    if data['variable_domain'] == 'spin':
        print_err('Error: unable to generate qubo data file from stdin, only boolean domains are supported by qubo')
        quit()

    print2out('c id : {}'.format(data['id']))

    if 'description' in data:
        print2out('c description : {}'.format(data['description']))
    print2out('c ')

    print2out('c scale : {}'.format(data['scale']))
    print2out('c offset : {}'.format(data['offset']))
    print2out('c ')

    for k in sorted(data['metadata']):
         print2out('c {} : {}'.format(k, json.dumps(data['metadata'][k], sort_keys=True)))
    if len(data['metadata']):
        print2out('c ')

    max_index = max(data['variable_ids'])+1 if len(data['variable_ids']) > 0 else 0
    num_diagonals = len(data['linear_terms'])
    num_elements = len(data['quadratic_terms'])

    print2out('p qubo 0 {} {} {}'.format(max_index, num_diagonals, num_elements))

    print2out('c linear terms')
    for term in data['linear_terms']:
        print2out('{} {} {}'.format(term['id'], term['id'], term['coeff']))

    print2out('c quadratic terms')
    for term in data['quadratic_terms']:
        print2out('{} {} {}'.format(term['id_tail'], term['id_head'], term['coeff']))


def bqpjson_to_mzn(data, out_stream):
    validate(data)

    print2out = partial(print, file=out_stream)

    print2out('% id : {}'.format(data['id']))

    if 'description' in data:
        print2out('% description : {}'.format(data['description']))
    print2out('% ')

    for k in sorted(data['metadata']):
         print2out('% {} : {}'.format(k, json.dumps(data['metadata'][k], sort_keys=True)))

    print2out('')
    if data['variable_domain'] == 'boolean':
        print2out('set of int: Domain = {0,1};')
    elif data['variable_domain'] == 'spin':
        print2out('set of int: Domain = {-1,1};')
    else:
        print_err('Error: unknown variable domain')
        quit()

    print2out('float: offset = {};'.format(data['offset']))
    print2out('float: scale = {};'.format(data['scale']))
    # this does not work becuose minizinc requires "array index set must be contiguous range"
    #var_ids_str = [str(var_id) for var_id in data['variable_id']]
    #print2out('set of int: Vars = {{{}}};'.format(','.join(var_ids_str)))

    print2out('')
    mzn_var = {}
    for var_id in data['variable_ids']:
        mzn_var[var_id] = 'x{}'.format(var_id)
        print2out('var Domain: {};'.format(mzn_var[var_id]))

    #print2out('array[Vars] of var Domain: x;')

    objective_terms = []
    for lt in data['linear_terms']:
        objective_terms.append('{}*{}'.format(lt['coeff'], mzn_var[lt['id']]))
    for qt in data['quadratic_terms']:
        objective_terms.append('{}*{}*{}'.format(qt['coeff'], mzn_var[qt['id_tail']], mzn_var[qt['id_head']]))

    # objective_terms = []
    # for lt in data['linear_terms']:
    #     objective_terms.append('{}*x[{}]'.format(lt['coeff'],lt['id']))
    # for qt in data['quadratic_terms']:
    #     objective_terms.append('{}*x[{}]*x[{}]'.format(qt['coeff'], qt['id_tail'], qt['id_head']))

    print2out('')
    objective_expr = ' + '.join(objective_terms) if len(objective_terms) > 0 else '0'
    print2out('var float: objective = {};'.format(objective_expr))

    print2out('')
    print2out('solve minimize objective;'.format(objective_expr))

    print2out('')
    var_list = []
    for var_id in data['variable_ids']:
        var_list.append(mzn_var[var_id])
    print2out('output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([{}])];'.format(', '.join(var_list)))

    # print2out('')
    # print2out('output [show(objective), " - ", show(x)]')
