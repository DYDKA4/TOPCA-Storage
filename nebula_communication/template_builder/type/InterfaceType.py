from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.NotificationDefinition import construct_notification_definition, \
    find_notification_definition_dependencies
from nebula_communication.template_builder.definition.OperationDefinition import construct_operation_definition, \
    find_operation_definition_dependencies
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType


def construct_interface_type(list_of_vid, only) -> dict:
    result = {}
    data_type = InterfaceType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'InterfaceType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'InterfaceType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'inputs':
                tmp_result['inputs'] = construct_property_definition(destination)
            elif edge == 'notifications':
                tmp_result['notifications'] = construct_notification_definition(destination)
            elif edge == 'operations':
                tmp_result['operations'] = construct_operation_definition(destination, only)
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_interface_type_dependencies(list_of_vid) -> dict:
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
    data_type = InterfaceType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'InterfaceType')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    dependencies = find_interface_type_dependencies(destination)
                    for key, value in dependencies.items():
                        result[key].union(value)
                    result['InterfaceType'].add(destination[0])
            elif edge == 'metadata':
                continue
            elif edge == 'inputs':
                dependencies = find_property_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'notifications':
                dependencies = find_notification_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'operations':
                dependencies = find_operation_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            else:
                print(edge)
                abort(500)

    return result
