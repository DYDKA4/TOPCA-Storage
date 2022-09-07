import json

from nebula_communication.nebula_functions import fetch_vertex


def construct_property_assignment(list_of_vid, only) -> dict:
    result = {}
    if only == 'attributes':
        return {}
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'PropertyAssignment')
        vertex_value = vertex_value.as_map()
        value: str = vertex_value['value'].as_string()
        if value.isnumeric():
            value: int = int(value)
        elif value.replace('.', '', 1).isdigit():
            value: float = float(value)
        else:
            try:
                value = json.loads(value)
            except ValueError:
                value = value
        result[vertex_value['name'].as_string()] = value
    return result
