from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination


def update_constraint_clause(father_node_vid, value, value_name, varargs: list):
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
    if value_name != 'value':
        abort(400)
    else:
        value_name = 'values'
    update_vertex('ConstraintClause', constraint_clause_vid_to_update, value_name, value)
