from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.ParameterDefinition import construct_parameter_definition
from parser.parser.tosca_v_1_3.definitions.ActivityDefinition import CallOperationActivityDefinition, \
    DelegateWorkflowActivityDefinition, SetStateActivityDefinition, InlineWorkflowActivityDefinition


def construct_activity_definition(list_of_vid) -> list:
    result = []

    for vid in list_of_vid:
        type_vertex = ''
        artifact_definition = {}
        if fetch_vertex(vid, 'CallOperationActivityDefinition'):
            artifact_definition = CallOperationActivityDefinition().__dict__
            type_vertex = 'CallOperationActivityDefinition'
        elif fetch_vertex(vid, 'DelegateWorkflowActivityDefinition'):
            artifact_definition = DelegateWorkflowActivityDefinition().__dict__
            type_vertex = 'DelegateWorkflowActivityDefinition'
        elif fetch_vertex(vid, 'SetStateActivityDefinition'):
            artifact_definition = SetStateActivityDefinition().__dict__
            type_vertex = 'SetStateActivityDefinition'
        elif fetch_vertex(vid, 'InlineWorkflowActivityDefinition'):
            artifact_definition = InlineWorkflowActivityDefinition().__dict__
            type_vertex = 'InlineWorkflowActivityDefinition'
        else:
            abort(500)
        vertex_value = fetch_vertex(vid, type_vertex)
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        if type_vertex == 'SetStateActivityDefinition':
            result.append({'set_state': vertex_value['set_state'].as_string()})
        edges = set(artifact_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'operation':
                if len(tmp_result.keys()) > 0 in range(0, 1) and 'inputs' in set(tmp_result.keys()):
                    operation = fetch_vertex(destination[0], 'OperationDefinition')
                    operation = operation.as_map()
                    operation = operation['name'].as_string()

                    tmp_result['operation'] = vertex_value['interface_name'].as_string() + '.' + operation
            elif edge == 'workflow':
                if len(tmp_result.keys()) > 0 in range(0, 1) and 'inputs' in set(tmp_result.keys()):
                    workflow = fetch_vertex(destination[0], 'ImperativeWorkflowDefinition')
                    workflow = workflow.as_map()
                    workflow = workflow['name'].as_string()
                    tmp_result['workflow'] = workflow
            elif edge == 'inputs':
                if len(tmp_result.keys()) in range(0, 1):
                    inputs = []
                    for inputs_value in destination:
                        inputs_value = fetch_vertex(inputs_value, 'ParameterDefinition')
                        inputs_value = inputs_value.as_map()
                        inputs_value = inputs_value['name'].as_string()
                        inputs.append(inputs_value)
                    tmp_result['inputs'] = inputs

                else:
                    abort(500)
            else:
                abort(500)
        if 'Delegate' in vertex_value['vertex_type_system'].as_string():
            name = 'delegate'
            result.append({name: tmp_result})
        elif 'Call' in vertex_value['vertex_type_system'].as_string():
            name = 'call_operation'
            result.append({name: tmp_result})
        elif 'Set' in vertex_value['vertex_type_system'].as_string():
            name = 'inline'
            result.append({name: tmp_result})
        elif 'Inline' not in vertex_value['vertex_type_system'].as_string():
            abort(500)
    return result
