from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from parser.parser.tosca_v_1_3.others.ConstraintСlause import ConstraintClause


def construct_constraint_schema(list_of_vid) -> list:
    result = []

    constraint_clause = ConstraintClause().__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ConstraintClause')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(constraint_clause.keys()) - set(vertex_keys) - {'vid'} - {'value'}
        if edges:
            print(edges, vid)
            abort(500)
        value = vertex_value['values'].as_string()
        value: str
        if value.isnumeric():
            value: int = int(value)
        elif value.replace('.', '', 1).isdigit():
            value: float = float(value)

        result.append({vertex_value['operator'].as_string(): value})
    return result
