from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.NotificationImplementationDefinition import \
    construct_notification_implementation_definition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition


def construct_notification_definition(list_of_vid) -> dict:
    result = {}

    property_definition = NotificationDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NotificationDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_value.keys():
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(property_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'implementation':
                tmp_result['implementation'] = construct_notification_implementation_definition(destination)
            elif edge == 'outputs':
                print(edge, destination)
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result
    return result
