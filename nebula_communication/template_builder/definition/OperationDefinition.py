from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.OperationImplementationDefinition import \
    construct_operation_implementation_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition


def construct_operation_definition(list_of_vid, only) -> dict:
    result = {}

    property_definition = OperationDefinition('name').__dict__

    for vid in list_of_vid:
        short_notation = ''
        vertex_value = fetch_vertex(vid, 'OperationDefinition')
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
                if destination:
                    data = fetch_vertex(destination[0], 'ArtifactDefinition')
                    if data is None:
                        tmp_result['implementation'] = construct_operation_implementation_definition(destination, only)
                    else:
                        primary = fetch_vertex(destination[0], 'ArtifactDefinition')
                        primary = primary.as_map()
                        primary = primary['name'].as_string()
                        short_notation = primary
            elif edge == 'outputs':
                if destination:
                    print(edge, destination)
            elif edge == 'inputs':
                if destination:
                    if fetch_vertex(destination[0], 'PropertyDefinition'):
                        tmp_result['inputs'] = construct_property_definition(destination)
                    elif fetch_vertex(destination[0], 'PropertyAssignment'):
                        tmp_result['inputs'] = construct_property_assignment(destination, only)
                    else:
                        abort(500)
            else:
                print(edge, destination)
                abort(500)
        if short_notation:
            result[vertex_value['name'].as_string()] = short_notation
        else:
            result[vertex_value['name'].as_string()] = tmp_result
    return result
