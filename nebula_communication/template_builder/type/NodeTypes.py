from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.ArtifactDefinition import construct_artifact_definition, \
    find_artifact_definition_dependencies
from nebula_communication.template_builder.definition.AttributeDefinition import construct_attribute_definition, \
    find_attribute_definition_dependencies
from nebula_communication.template_builder.definition.CapabilityDefinition import construct_capability_definition, \
    find_capability_definition_dependencies
from nebula_communication.template_builder.definition.InterfaceDefinition import construct_interface_definition, \
    find_interface_definition_dependencies
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from nebula_communication.template_builder.definition.RequirementDefinition import construct_requirement_definition, \
    find_requirement_definition_dependencies
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


def construct_node_type(list_of_vid, only) -> dict:
    result = {}
    node_type = NodeType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NodeType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(node_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'NodeType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_definition(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_definition(destination)
            elif edge == 'requirements':
                tmp_result['requirements'] = construct_requirement_definition(destination, only)
            elif edge == 'interfaces':
                tmp_result['interfaces'] = construct_interface_definition(destination, only)
            elif edge == 'capabilities':
                tmp_result['capabilities'] = construct_capability_definition(destination)
            elif edge == 'artifacts':
                tmp_result['artifacts'] = construct_artifact_definition(destination, only)
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_node_type_dependencies(list_of_vid) -> dict:
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
    node_type = NodeType('name').__dict__
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NodeType')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(node_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    dependencies = find_node_type_dependencies(destination)
                    for key, value in dependencies.items():
                        result[key].union(value)
                    result['NodeType'].add(destination[0])
            elif edge == 'metadata':
                continue
            elif edge == 'properties':
                dependencies = find_property_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'attributes':
                dependencies = find_attribute_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'requirements':
                dependencies = find_requirement_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'interfaces':
                dependencies = find_interface_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'capabilities':
                dependencies = find_capability_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'artifacts':
                dependencies = find_artifact_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            else:
                print(edge)
                abort(500)

    return result


