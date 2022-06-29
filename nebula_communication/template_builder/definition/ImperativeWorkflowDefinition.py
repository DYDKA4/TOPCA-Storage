from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.OperationImplementationDefinition import \
    construct_operation_implementation_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition
from nebula_communication.template_builder.definition.WorkflowPreconditionDefinition import \
    construct_workflow_precondition_definition
from nebula_communication.template_builder.definition.WorkflowStepDefinition import construct_workflow_step_definition
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition


def construct_imperative_workflow_definition(list_of_vid) -> dict:
    result = {}
    imperative_workflow_definition = ImperativeWorkflowDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ImperativeWorkflowDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(imperative_workflow_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            if edge == 'steps':
                edge = 'steps_tosca'
            destination = find_destination(vid, edge)
            if edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'inputs':
                tmp_result['inputs'] = construct_property_definition(destination)
            elif edge == 'preconditions':
                tmp_result['preconditions'] = construct_workflow_precondition_definition(destination)
            elif edge == 'steps_tosca':
                tmp_result['steps'] = construct_workflow_step_definition(destination)
            elif edge == 'implementation':
                tmp_result['implementation'] = construct_operation_implementation_definition(destination)
            elif edge == 'outputs':
                print(edge, destination)  # todo Make it Later
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
