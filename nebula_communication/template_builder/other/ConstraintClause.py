import json

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
        value: str = vertex_value['value'].as_string()
        try:
            value = json.loads(value)
        except ValueError:
            continue
        if type(value) == str:
            if value.isnumeric():
                value: int = int(value)
            elif value.replace('.', '', 1).isdigit():
                value: float = float(value)
            elif value[0] == '[' and value[-1] == ']':
                value: str = value[1:-1]
                value: list = value.split(',')
                for index, item in enumerate(value):
                    while (item[0] == item[-1] and item[0] in {'"', "'"}) or item[0] == ' ':
                        if item[0] == ' ':
                            item = item[1:]
                        else:
                            item = item[1:-1]
                    value[index] = item
                    if item.isnumeric():
                        value[index] = int(item)
                    elif item.replace('.', '', 1).isdigit():
                        value[index] = float(item)
        result.append({vertex_value['operator'].as_string(): value})
    return result
