from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.AttributeAssignment import construct_attribute_assignment
from nebula_communication.template_builder.assignment.CapabilityAssignment import construct_capability_assignment
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.assignment.RequirementAssignment import construct_requirement_assignment
from nebula_communication.template_builder.definition.ArtifactDefinition import construct_artifact_definition
from nebula_communication.template_builder.definition.AttributeDefinition import construct_attribute_definition
from nebula_communication.template_builder.definition.CapabilityDefinition import construct_capability_definition
from nebula_communication.template_builder.definition.InterfaceDefinition import construct_interface_definition
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.NodeFilterDefinition import construct_node_filter_definition
from nebula_communication.template_builder.definition.RequirementDefinition import construct_requirement_definition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate


def construct_node_template(list_of_vid) -> dict:
    result = {}
    node_type = NodeTemplate('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NodeTemplate')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(node_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                derived_from = fetch_vertex(destination[0], 'NodeType')
                derived_from = derived_from.as_map()
                derived_from = derived_from['name'].as_string()
                tmp_result['type'] = derived_from
            elif edge == 'directives':
                directives = []
                for directive in destination:
                    directive = fetch_vertex(directive, 'Directives')
                    directive = directive.as_map()
                    directive = directive['values'].as_string()
                    directives.append(directive)
                tmp_result['directives'] = directives
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_assignment(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_assignment(destination)
            elif edge == 'requirements':
                tmp_result['requirements'] = construct_requirement_assignment(destination)
            elif edge == 'interfaces':
                tmp_result['interfaces'] = construct_interface_definition(destination)
            elif edge == 'capabilities':
                tmp_result['capabilities'] = construct_capability_assignment(destination)
            elif edge == 'artifacts':
                tmp_result['artifacts'] = construct_artifact_definition(destination)
            elif edge == 'node_filter':
                tmp_result['node_filter'] = construct_node_filter_definition(destination)
            elif edge == 'copy':
                print(edge, destination)
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
