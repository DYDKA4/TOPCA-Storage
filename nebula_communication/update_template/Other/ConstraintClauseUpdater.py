from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination, delete_vertex, \
    add_in_vertex, add_edge
from parser.parser.tosca_v_1_3.others.ConstraintСlause import ConstraintClause

def start_constraint_clause(father_node_vid, varargs):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    constraint_clause_vid_to_update = None
    for constraint_clause_vid in destination:
        constraint_clause_value = fetch_vertex(constraint_clause_vid, 'ConstraintClause')
        constraint_clause_value = constraint_clause_value.as_map()
        if constraint_clause_value.get('operator').as_string() == varargs[1]:
            constraint_clause_vid_to_update = constraint_clause_vid
            break
    if constraint_clause_vid_to_update is None:
        abort(400)
    return constraint_clause_vid_to_update
def update_constraint_clause(father_node_vid, value, value_name, varargs: list, type_update):
    constraint_clause_vid_to_update = start_constraint_clause(father_node_vid, varargs)
    if type_update == 'delete':
        delete_vertex('"' + constraint_clause_vid_to_update.as_string() + '"')
        return
    if value_name != 'value':
        abort(400)
    else:
        value_name = 'values'
    update_vertex('ConstraintClause', constraint_clause_vid_to_update, value_name, value)


def add_constraint_clause(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add':
        constraint_clause = ConstraintClause()
        constraint_clause.operator = '"' + varargs[0] + '"'
        generate_uuid(constraint_clause, cluster_name)
        add_in_vertex(constraint_clause.vertex_type_system, 'operator, vertex_type_system',
                      constraint_clause.operator + ',"' + constraint_clause.vertex_type_system + '"',
                      constraint_clause.vid)
        add_edge(edge_name, '', parent_vid, constraint_clause.vid, '')
        return True
    return False


def get_constraint_clause(father_node_vid, value, value_name, varargs: list):
    constraint_clause_vid_to_update = start_constraint_clause(father_node_vid, varargs)
    constraint_value = fetch_vertex(constraint_clause_vid_to_update, 'PropertyAssignment')
    constraint_value = constraint_value.as_map()
    if value_name in constraint_value.keys():
        if value == constraint_value.get(value_name).as_string():
            return constraint_clause_vid_to_update.as_string()
    else:
        abort(400)


