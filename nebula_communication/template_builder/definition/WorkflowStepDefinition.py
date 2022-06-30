from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.ActivityDefinition import construct_activity_definition
from nebula_communication.template_builder.definition.ConditionClauseDefinition import \
    construct_condition_clause_definition
from parser.parser.tosca_v_1_3.definitions.WorkflowStepDefinition import WorkflowStepDefinition


def construct_workflow_step_definition(list_of_vid) -> dict:
    result = {}
    imperative_workflow_definition = WorkflowStepDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'WorkflowStepDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(imperative_workflow_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'target':
                target = None
                if fetch_vertex(destination[0], 'NodeTemplate'):
                    target = fetch_vertex(destination[0], 'NodeTemplate')
                elif fetch_vertex(destination[0], 'GroupDefinition'):
                    target = fetch_vertex(destination[0], 'GroupDefinition')
                else:
                    abort(500)
                target = target.as_map()
                target = target['name'].as_string()
                tmp_result['target'] = target
            elif edge == 'target_relationship':
                if destination[0]:
                    target_relationship = fetch_vertex(destination[0], 'RelationshipTemplate')
                    target_relationship = target_relationship.as_map()
                    target_relationship = target_relationship['name'].as_string()
                    tmp_result['target_relationship'] = target_relationship
            elif edge == 'filter':
                filters = []
                for filter_condition in destination:
                    filters.append(construct_condition_clause_definition([filter_condition]))
                tmp_result['filter'] = filters
            elif edge == 'activities':
                tmp_result['activities'] = construct_activity_definition(destination)
            elif edge == 'on_success':
                on_success_list = []
                for on_success in destination:
                    on_success = fetch_vertex(on_success, 'WorkflowStepDefinition')
                    on_success = on_success.as_map()
                    on_success = on_success['name'].as_string()
                    on_success_list.append(on_success)
                tmp_result['on_success'] = on_success_list
            elif edge == 'on_failure':
                on_failure_list = []
                for on_failure in destination:
                    on_failure = fetch_vertex(on_failure, 'WorkflowStepDefinition')
                    on_failure = on_failure.as_map()
                    on_failure = on_failure['name'].as_string()
                    on_failure_list.append(on_failure)
                tmp_result['on_failure'] = on_failure_list
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
