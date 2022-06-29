from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.CapabilityFilterDefinition import \
    construct_capability_filter_definition
from nebula_communication.template_builder.definition.NotificationImplementationDefinition import \
    construct_notification_implementation_definition
from nebula_communication.template_builder.definition.PropertyFilterDefinition import \
    construct_property_filter_definition
from parser.parser.tosca_v_1_3.definitions.NodeFilterDefinition import NodeFilterDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition


def construct_node_filter_definition(list_of_vid) -> dict:
    result = {}

    property_definition = NodeFilterDefinition().__dict__
    if len(list_of_vid) > 1:
        abort(500)
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NodeFilterDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        edges = set(property_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'properties':
                tmp_result['properties'] = construct_property_filter_definition(destination)
            elif edge == 'capabilities':
                tmp_result['capabilities'] = construct_capability_filter_definition(destination)
            else:
                abort(500)
        result = tmp_result
    return result
