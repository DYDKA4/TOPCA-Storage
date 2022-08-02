from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex
from nebula_communication.update_template.Definition.GroupDefinitionUpdater import update_group_definition, \
    add_group_definition, get_group_definition
from nebula_communication.update_template.Definition.ImperativeWorkflowDefinition import \
    update_imperative_workflow_definition, add_imperative_workflow_definition, get_imperative_workflow_definition
from nebula_communication.update_template.Definition.ParameterDefinitionUpdater import update_parameter_definition, \
    add_parameter_definition, get_parameter_definition
from nebula_communication.update_template.Definition.PolicyDefinitionUpdater import update_policy_definition, \
    add_policy_definition, get_policy_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from nebula_communication.update_template.Other.NodeTemplateUpdater import update_node_template, add_node_template, \
    get_node_template
from nebula_communication.update_template.Other.RelationshipTemplateUpdater import update_relationship_template, \
    add_relationship_template, get_relationship_template
from nebula_communication.update_template.find_functions import return_all


def update_topology_template_definition(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
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
        if not add_metadata(type_update, varargs[1:], value, value_name, cluster_name, topology_template_definition):
            update_metadata(topology_template_definition, value, value_name, varargs[1:], type_update)
    elif varargs[1] == 'inputs':
        if not add_parameter_definition(type_update, varargs[1:], cluster_name, topology_template_definition,
                                        varargs[1:]):
            update_parameter_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                        type_update, cluster_name)
    elif varargs[1] == 'outputs':
        if not add_parameter_definition(type_update, varargs[1:], cluster_name, topology_template_definition,
                                        varargs[1:]):
            update_parameter_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                        type_update, cluster_name)
    elif varargs[1] == 'node_template':
        if not add_node_template(type_update, varargs[1:], cluster_name, topology_template_definition, varargs[1:]):
            update_node_template(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                 type_update, cluster_name)
    elif varargs[1] == 'relationship_templates':
        if not add_relationship_template(type_update, varargs[1:], cluster_name, topology_template_definition,
                                         varargs[1]):
            update_relationship_template(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                         type_update, cluster_name)
    elif varargs[1] == 'groups':
        if not add_group_definition(type_update, varargs[1:], cluster_name, topology_template_definition,
                                    varargs[1]):
            update_group_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                    type_update, cluster_name)
    elif varargs[1] == 'policies':
        if not add_policy_definition(type_update, varargs[1:], cluster_name, topology_template_definition, varargs[1]):
            update_policy_definition(father_node_vid, topology_template_definition, value, value_name, varargs[1:],
                                     type_update, cluster_name)
    elif varargs[1] == 'workflows':
        if not add_imperative_workflow_definition(type_update, varargs[1:], cluster_name, topology_template_definition,
                                                  varargs[1]):
            update_imperative_workflow_definition(father_node_vid, topology_template_definition, value, value_name,
                                                  varargs[1:],type_update, cluster_name)
    else:
        abort(400)


def get_topology_template_definition(father_node_vid, value, value_name, varargs: list):
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
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_metadata(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'inputs':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_parameter_definition(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'outputs':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_parameter_definition(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'node_templates':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_node_template(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'relationship_templates':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_relationship_template(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'groups':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_group_definition(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'policies':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_policy_definition(topology_template_definition, value, value_name, varargs[1:])
    elif varargs[1] == 'workflows':
        destination = find_destination(topology_template_definition, varargs[1])
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_imperative_workflow_definition(topology_template_definition, value, value_name, varargs[1:])
    else:
        abort(400)
