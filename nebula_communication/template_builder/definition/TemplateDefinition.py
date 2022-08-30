from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.GroupDefinition import construct_group_definition
from nebula_communication.template_builder.definition.ImperativeWorkflowDefinition import \
    construct_imperative_workflow_definition
from nebula_communication.template_builder.definition.ParameterDefinition import construct_parameter_definition
from nebula_communication.template_builder.definition.PolicyDefinition import construct_policy_definition
from nebula_communication.template_builder.other.NodeTemplate import construct_node_template
from nebula_communication.template_builder.other.RelationshipTemplate import construct_relationship_template
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def construct_topology_template_definition(list_of_vid, only) -> dict:
    result = {}
    topology_template_definition = TemplateDefinition().__dict__

    if len(list_of_vid) > 1:
        abort(500)
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'TopologyTemplateDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(topology_template_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'inputs':
                tmp_result['inputs'] = construct_parameter_definition(destination)

            elif edge == 'outputs':
                tmp_result['outputs'] = construct_parameter_definition(destination)
            elif edge == 'node_templates':
                tmp_result['node_templates'] = construct_node_template(destination, only)
            elif edge == 'relationship_templates':
                tmp_result['relationship_templates'] = construct_relationship_template(destination, only)
            elif edge == 'groups':
                tmp_result['groups'] = construct_group_definition(destination, only)
            elif edge == 'policies':
                tmp_result['policies'] = construct_policy_definition(destination, only)
            elif edge == 'workflows':
                tmp_result['workflows'] = construct_imperative_workflow_definition(destination, only)
            elif edge == 'substitution_mappings':
                print(edge, destination)  # todo Make it later
            else:
                print(edge)
                abort(500)
        result = tmp_result

    return result
