from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.NotificationDefinition import construct_notification_definition, \
    find_notification_definition_dependencies
from nebula_communication.template_builder.definition.OperationDefinition import construct_operation_definition, \
    find_operation_definition_dependencies
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from nebula_communication.template_builder.type.InterfaceType import find_interface_type_dependencies
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition


def construct_interface_definition(list_of_vid, only) -> dict:
    result = {}
    data_type = InterfaceDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'InterfaceDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                interface_type = fetch_vertex(destination[0], 'InterfaceType')
                interface_type = interface_type.as_map()
                interface_type = interface_type['name'].as_string()
                tmp_result['type'] = interface_type
            elif edge == 'inputs':
                if destination:
                    if fetch_vertex(destination[0], 'PropertyDefinition'):
                        tmp_result['inputs'] = construct_property_definition(destination)
                    elif fetch_vertex(destination[0], 'PropertyAssignment'):
                        tmp_result['inputs'] = construct_property_assignment(destination, only)
            elif edge == 'notifications':
                tmp_result['notifications'] = construct_notification_definition(destination)
            elif edge == 'operations':
                tmp_result['operations'] = construct_operation_definition(destination, only)
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_interface_definition_dependencies(list_of_vid, result) -> dict:
    if result is None:
        result = {
            'ArtifactType': set(),
            'CapabilityType': set(),
            'DataType': set(),
            'GroupType': set(),
            'InterfaceType': set(),
            'NodeType': set(),
            'PolicyType': set(),
            'RelationshipType': set(),
        }
    data_type = InterfaceDefinition('name').__dict__
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'InterfaceDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                dependencies = find_interface_type_dependencies(destination, result)
                for key, value in dependencies.items():
                    result[key].union(value)
                result['InterfaceType'].add(destination[0])
            elif edge == 'inputs':
                if destination:
                    if fetch_vertex(destination[0], 'PropertyDefinition'):
                        dependencies = find_property_definition_dependencies(destination, result)
                        for key, value in dependencies.items():
                            result[key].union(value)
                    elif fetch_vertex(destination[0], 'PropertyAssignment'):
                        continue
            elif edge == 'notifications':
                dependencies = find_notification_definition_dependencies(destination, result)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'operations':
                dependencies = find_operation_definition_dependencies(destination, result)
                for key, value in dependencies.items():
                    result[key].union(value)
            else:
                print(edge)
                abort(500)
    return result
