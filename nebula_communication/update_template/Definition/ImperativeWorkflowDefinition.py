from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment, get_property_assignment
from nebula_communication.update_template.Assignment.RequirementAssignment import return_all
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import get_attribute_definition
from nebula_communication.update_template.Definition.OperationImplementationDefinitionUpdater import \
    update_operation_implementation_definition, add_operation_implementation_definition, \
    get_operation_implementation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import get_property_definition
from nebula_communication.update_template.Definition.WorkflowPreconditionDefinitionUpdater import \
    update_workflow_precondition_definition, add_workflow_precondition_definition, get_workflow_precondition_definition
from nebula_communication.update_template.Definition.WorkflowStepDefinitionUpdater import \
    update_workflow_step_definition, add_workflow_step_definition, get_workflow_step_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition


def start_imperative_workflow_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    imperative_workflow_vid_to_update = None
    for imperative_workflow_vid in destination:
        imperative_workflow_value = fetch_vertex(imperative_workflow_vid, 'ImperativeWorkflowDefinition')
        imperative_workflow_value = imperative_workflow_value.as_map()
        if imperative_workflow_value.get('name').as_string() == varargs[1]:
            imperative_workflow_vid_to_update = imperative_workflow_vid
            break
    if imperative_workflow_vid_to_update is None:
        abort(400)
    return imperative_workflow_vid_to_update


def update_imperative_workflow_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                          type_update, cluster_name):
    imperative_workflow_vid_to_update = start_imperative_workflow_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + imperative_workflow_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(imperative_workflow_vid_to_update, 'ImperativeWorkflowDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('ImperativeWorkflowDefinition', imperative_workflow_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name,
                            imperative_workflow_vid_to_update):
            update_metadata(imperative_workflow_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'inputs':
        if not add_property_assignment(type_update, varargs[2:], value, value_name, cluster_name,
                                       imperative_workflow_vid_to_update):
            update_property_assignment(service_template_vid, imperative_workflow_vid_to_update, value, value_name,
                                       varargs[2:], type_update)
    elif varargs[2] == 'preconditions':
        if not add_workflow_precondition_definition(type_update, varargs[2:], cluster_name,
                                                    imperative_workflow_vid_to_update, varargs[2]):
            update_workflow_precondition_definition(service_template_vid, imperative_workflow_vid_to_update, value,
                                                    value_name, varargs[2:], type_update)
    elif varargs[2] == 'steps':
        if not add_workflow_step_definition(type_update, varargs[2:], cluster_name, imperative_workflow_vid_to_update,
                                            varargs[2]):
            update_workflow_step_definition(service_template_vid, imperative_workflow_vid_to_update, value, value_name,
                                            varargs[2:], type_update)
    elif varargs[2] == 'implementation':
        if not add_operation_implementation_definition(type_update, varargs[2:], cluster_name,
                                                       imperative_workflow_vid_to_update,
                                                       varargs[2]):
            update_operation_implementation_definition(service_template_vid, imperative_workflow_vid_to_update, value,
                                                       value_name, varargs[2:], type_update, cluster_name)
    else:
        abort(400)


def add_imperative_workflow_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = ImperativeWorkflowDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_imperative_workflow_definition(father_node_vid, value, value_name, varargs: list):
    imperative_workflow_vid_to_update = start_imperative_workflow_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(imperative_workflow_vid_to_update, 'ImperativeWorkflowDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return imperative_workflow_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        destination = find_destination(imperative_workflow_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_metadata(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'inputs':
        destination = find_destination(imperative_workflow_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_property_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'preconditions':
        destination = find_destination(imperative_workflow_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_workflow_precondition_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'steps':
        destination = find_destination(imperative_workflow_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_workflow_step_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'implementation':
        destination = find_destination(imperative_workflow_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_operation_implementation_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
