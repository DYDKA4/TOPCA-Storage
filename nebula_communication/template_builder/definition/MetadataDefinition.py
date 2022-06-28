from nebula_communication.nebula_functions import fetch_vertex


def construct_metadata_definition(list_of_vid) -> dict:
    result = {}

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'Metadata')
        vertex_value = vertex_value.as_map()
        result[vertex_value['name'].as_string()] = vertex_value['values'].as_string()
    return result
