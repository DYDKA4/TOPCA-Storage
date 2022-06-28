from nebula_communication.nebula_functions import fetch_vertex


def construct_import_definition(list_of_vid) -> list:
    result = []

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ImportDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        for vertex_key in vertex_value.keys():
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        result.append(tmp_result)
    return result
