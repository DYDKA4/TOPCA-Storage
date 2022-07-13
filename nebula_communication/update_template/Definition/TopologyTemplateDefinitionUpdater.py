from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.GroupDefinitionUpdater import update_group_definition
from nebula_communication.update_template.Definition.ImperativeWorkflowDefinition import \
    update_imperative_workflow_definition
from nebula_communication.update_template.Definition.ParameterDefinitionUpdater import update_parameter_definition
from nebula_communication.update_template.Definition.PolicyDefinitionUpdater import update_policy_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata
from nebula_communication.update_template.Other.NodeTemplateUpdater import update_node_template
from nebula_communication.update_template.Other.RelationshipTemplateUpdater import update_relationship_template


def update_topology_template_definition(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 1:
        abort(400)
    topology_template_definition = find_destination(father_node_vid, varargs[0])
    if topology_template_definition is None or len(topology_template_definition) > 1:
        abort(400)
    topology_template_definition = topology_template_definition[0]
    if len(varargs) == 1:
        vertex_value = fetch_vertex(topology_template_definition, 'TopologyTemplateDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('TopologyTemplateDefinition', topology_template_definition, value_name, value)
        else:
            abort(400)
    elif varargs[1] == 'metadata':
        update_metadata(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'inputs':
        update_parameter_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'outputs':
        update_parameter_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'node_template':
        update_node_template(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'relationship_templates':
        update_relationship_template(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'groups':
        update_group_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'policies':
        update_policy_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'workflows':
        update_imperative_workflow_definition(father_node_vid, topology_template_definition, value, value_name,
                                              varargs[1:])
    else:
        abort(400)
