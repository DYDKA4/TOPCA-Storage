import json

from nebula_communication.nebula_functions import fetch_vertex


def construct_attribute_assignment(list_of_vid, only) -> dict:
    result = {}
    if only == 'properties':
        return {}
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'AttributeAssignment')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                value: str = vertex_value['values'].as_string()
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
                tmp_result['value'] = value

        result[vertex_value['name'].as_string()] = tmp_result
    return result
