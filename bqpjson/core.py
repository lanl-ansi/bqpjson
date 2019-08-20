from __future__ import print_function

import os, sys, json, copy, math

from io import IOBase
import fractions
import itertools
import functools

import jsonschema

# prints a line to standard error
print_err = functools.partial(print, file=sys.stderr)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bqpjson-schema.json')) as file:
    _qbpjson_schema = json.load(file)

_bqpjson_versions = ['1.0.0']
_bqpjson_version_latest = _bqpjson_versions[-1]


def validate(data):
    jsonschema.validate(data, _qbpjson_schema)

    assert(data['version'] == _bqpjson_version_latest)

    assert(data['scale'] >= 0.0)

    var_ids = {i for i in data['variable_ids']}
    lt_vars = set([])
    for lt in data['linear_terms']:
        assert(lt['id'] in var_ids)
        assert(lt['id'] not in lt_vars)
        lt_vars.add(lt['id'])

    qt_var_pairs = set()
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
        spin_var_domain = data['variable_domain'] == 'spin'
        boolean_var_domain = data['variable_domain'] == 'boolean'
        solution_ids = set()
        for solution in data['solutions']:
            assert(solution['id'] not in solution_ids)
            solution_ids.add(solution['id'])

            sol_var_ids = set()
            for assign in solution['assignment']:
                var_id = assign['id']
                assert(var_id in var_ids)
                assert(var_id not in sol_var_ids)
                sol_var_ids.add(var_id)
                if spin_var_domain:
                    assert(assign['value'] == -1 or assign['value'] == 1)
                if boolean_var_domain:
                    assert(assign['value'] == 0 or assign['value'] == 1)
            assert(len(sol_var_ids) == len(var_ids))


def evaluate(data):
    validate(data)

    values = []
    if 'solutions' in data:
        for solution in data['solutions']:
            assignment = {item['id']:item['value'] for item in solution['assignment']}
            values.append(_evaluate(data, assignment))

    return values


def _evaluate(data, assignment):
    value = data['offset'] \
        + sum(lt['coeff']*assignment[lt['id']] for lt in data['linear_terms']) \
        + sum(qt['coeff']*assignment[qt['id_tail']]*assignment[qt['id_head']] for qt in data['quadratic_terms'])

    return data['scale']*value


def swap_variable_domain(data):
    validate(data)
    if data['variable_domain'] == 'spin':
        output_data = spin_to_bool(data)
    else:
        assert(data['variable_domain'] == 'boolean')
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
        #assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = 2.0*coeff
        offset += -coeff

    for quadratic_term in ising_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        coeff = quadratic_term['coeff']
        #assert(coeff != 0.0)

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
        #assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = coeff/2.0
        offset += linear_term['coeff']/2.0

    for quadratic_term in bool_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        coeff = quadratic_term['coeff']
        #assert(coeff != 0.0)

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

    print2out = functools.partial(print, file=out_stream)

    if data['variable_domain'] == 'boolean':
        print_err('Error: unable to generate qubist hamiltonian, only spin domains are supported by qubist')
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

    print2out = functools.partial(print, file=out_stream)

    if data['variable_domain'] == 'spin':
        print_err('Error: unable to generate qubo data file, only boolean domains are supported by qubo')
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


def bqpjson_to_minizinc(data, out_stream):
    validate(data)

    print2out = functools.partial(print, file=out_stream)

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



def bqpjson_to_hfs(data, out_stream, chimera_cell_size=None, chimera_degree=None, precision=5):
    '''
    Format description from (https://github.com/alex1770/QUBO-Chimera)

    The format of the instance-description file starts with a line giving the 
    size of the Chimera graph. (Two numbers are given to specify an m x n
    rectangle, but currently only a square, m=n, is accepted.)
    The subsequent lines are of the form
        <Chimera vertex> <Chimera vertex> weight
    where <Chimera vertex> is specified by four numbers using the format,

    Chimera graph, C_N:
        Vertices are (x,y,o,i)  0<=x,y<N, 0<=o<2, 0<=i<4
        Edge from (x,y,o,i) to (x',y',o',i') if
        (x,y)=(x',y'), o!=o', OR
        |x-x'|=1, y=y', o=o'=0, i=i', OR
        |y-y'|=1, x=x', o=o'=1, i=i'
         
        x,y are the horizontal,vertical co-ords of the K4,4
        o=0..1 is the "orientation" (0=horizontally connected, 1=vertically connected)
        i=0..3 is the index within the "semi-K4,4"="bigvertex"
        There is an involution given by {x<->y o<->1-o}
    '''
    validate(data)

    print2out = functools.partial(print, file=out_stream)

    if data['variable_domain'] == 'spin':
        print_err('Error: unable to generate hfs data file, only boolean domains are supported by this translator')
        quit()

    if len(data['variable_ids']) <= 0:
        print_err('WARNING: hfs data file with no data')
        print2out('0 0')
        return 0.0, 0.0
        #quit()

    if 'chimera_cell_size' in data['metadata'] and chimera_cell_size == None:
        chimera_cell_size = data['metadata']['chimera_cell_size']

    if 'chimera_degree' in data['metadata'] and chimera_degree == None:
        chimera_degree = data['metadata']['chimera_degree']

    if chimera_cell_size == None:
        chimera_cell_size = 8
        print_err('WARNING: chimera_cell_size parameter not found, assuming {}'.format(chimera_cell_size))

    min_chimera_degree = int(math.ceil(math.sqrt(max(data['variable_ids'])/float(chimera_cell_size))))
    if chimera_degree == None:
        chimera_degree = min_chimera_degree
        print_err('WARNING: chimera_degree parameter not found, assuming {}'.format(chimera_degree))

    if chimera_degree < min_chimera_degree:
        print_err('Error: chimera_degree of {} was specified.  However, the minimum chimera_degree of {} is required for a problem with a variable index of {}'.format(chimera_degree, min_chimera_degree, max(data['variable_ids'])))
        quit()

    chimera_cell_row_size = chimera_cell_size // 2


    # These values are used to transform a variable index into a chimera 
    # coordinate (x,y,o,i)
    # x - chimera_row
    # y - chimera_column
    # o - chimera_cell_column - indicates the first or the second row of a chimera cell
    # i - chimera_cell_column_id - indicates ids within a chimera cell
    # Note that knowing the size of source chimera graph is essential to doing this mapping correctly 
    #
    chimera_cell_column = {index: (index % chimera_cell_size) // chimera_cell_row_size for index in data['variable_ids']}
    chimera_cell_column_id = {index:index % chimera_cell_row_size for index in data['variable_ids']}
    chimera_cell = {index:index // chimera_cell_size for index in data['variable_ids']}
    chimera_row = {index:chimera_cell_id // chimera_degree for index, chimera_cell_id in chimera_cell.items()}
    chimera_column = {index:chimera_cell_id % chimera_degree for index, chimera_cell_id in chimera_cell.items()}

    chimera_coordinate = {index:(chimera_row[index], chimera_column[index], chimera_cell_column[index], chimera_cell_column_id[index]) for index in data['variable_ids']}


    chimera_degree_effective = max(max(chimera_row.values()), max(chimera_column.values())) + 1

    print_err('hfs data parameters:')
    print_err('  chimera_cell_size: {}'.format(chimera_cell_size))
    print_err('  chimera_cell_row_size: {}'.format(chimera_cell_row_size))
    print_err('  chimera_degree: {}'.format(chimera_degree))
    print_err('  chimera_degree_effective: {}'.format(chimera_degree_effective))

    assert(chimera_degree_effective <= chimera_degree)

    max_abs_coeff = max(abs(t['coeff']) for t in itertools.chain(data['linear_terms'], data['quadratic_terms']))
    scale = 10 ** precision / max_abs_coeff

    for term in itertools.chain(data['linear_terms'], data['quadratic_terms']):
        term['int_coeff'] = round(term['coeff'] * scale)

    print_err('INFO: scaling factor {} offset {}'.format(data['scale']/scale, data['offset']*scale))

    # Output the hfs data file
    # it is a header followed by linear terms and then quadratic terms
    print2out('%d %d' % (chimera_degree_effective, chimera_degree_effective))
    for lt in data['linear_terms']:
        idx = lt['id']
        weight = lt['int_coeff']
        args = chimera_coordinate[idx] + chimera_coordinate[idx] + tuple([weight])
        print2out('%2d %2d %2d %2d    %2d %2d %2d %2d    %8d' % args)

    for qt in data['quadratic_terms']:
        idx_t = qt['id_tail']
        idx_h = qt['id_head']
        weight = qt['int_coeff']
        args = chimera_coordinate[idx_t] + chimera_coordinate[idx_h] + tuple([weight])
        print2out('%2d %2d %2d %2d    %2d %2d %2d %2d    %8d' % args)

    return data['scale']/scale, data['offset']*scale


# Greatest common divisor of more than 2 numbers
def _gcd(*numbers):
    return functools.reduce(fractions.gcd, numbers)

# Least common multiple of more than 2 numbers:
def _lcm(*numbers):
    def lcm(a, b):
        return (a * b) // _gcd(a, b)
    return functools.reduce(lcm, numbers, 1)

