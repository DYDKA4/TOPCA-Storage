from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment
from nebula_communication.update_template.Definition.OperationImplementationDefinitionUpdater import \
    update_operation_implementation_definition
from nebula_communication.update_template.Definition.WorkflowPreconditionDefinitionUpdater import \
    update_workflow_precondition_definition
from nebula_communication.update_template.Definition.WorkflowStepDefinitionUpdater import \
    update_workflow_step_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences


def update_imperative_workflow_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
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
    if len(varargs) == 2:
        vertex_value = fetch_vertex(imperative_workflow_vid_to_update, 'ImperativeWorkflowDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('ImperativeWorkflowDefinition', imperative_workflow_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        update_metadata(imperative_workflow_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'inputs':
        update_property_assignment(service_template_vid, imperative_workflow_vid_to_update, value, value_name,
                                   varargs[2:])
    elif varargs[2] == 'preconditions':
        update_workflow_precondition_definition(service_template_vid, imperative_workflow_vid_to_update, value,
                                                value_name, varargs[2:])
    elif varargs[2] == 'steps':
        update_workflow_step_definition(service_template_vid, imperative_workflow_vid_to_update, value, value_name,
                                        varargs[2:])
    elif varargs[2] == 'implementation':
        update_operation_implementation_definition(service_template_vid, imperative_workflow_vid_to_update, value,
                                                   value_name, varargs[2:])
    else:
        abort(400)
