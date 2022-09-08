from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.AttributeDefinition import construct_attribute_definition, \
    find_attribute_definition_dependencies
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from parser.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


def construct_capability_type(list_of_vid) -> dict:
    result = {}
    capability_type = CapabilityType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'CapabilityType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(capability_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'CapabilityType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_definition(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_definition(destination)
            elif edge == 'valid_source_types':
                valid_source_types = []
                for valid_source_type in destination:
                    data = fetch_vertex(valid_source_type, 'NodeType')
                    data = data.as_map()
                    valid_source_types.append(data['name'].as_string())
                tmp_result['valid_source_types'] = valid_source_types
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_capability_type_dependencies(list_of_vid) -> dict:
    from nebula_communication.template_builder.type.NodeTypes import find_node_type_dependencies
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
    capability_type = CapabilityType('name').__dict__
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'CapabilityType')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(capability_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    dependencies = find_capability_type_dependencies(destination)
                    for key, value in dependencies.items():
                        result[key].union(value)
                    result['CapabilityType'].add(destination[0])
            elif edge == 'properties':
                dependencies = find_property_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'attributes':
                dependencies = find_attribute_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'valid_source_types':
                dependencies = find_node_type_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
                for vertex in destination:
                    result['NodeType'].add(vertex)
            elif edge == 'metadata':
                continue
            else:
                abort(500)
    return result
