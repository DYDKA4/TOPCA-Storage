from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.ActivityDefinition import construct_activity_definition
from nebula_communication.template_builder.definition.ConditionClauseDefinition import \
    construct_condition_clause_definition

from nebula_communication.template_builder.definition.EventFilterDefinition import construct_event_filter_definition
from parser.parser.tosca_v_1_3.definitions.TriggerDefinition import TriggerDefinition


def construct_trigger_definition(list_of_vid) -> dict:
    result = {}
    trigger_definition = TriggerDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'TriggerDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        condition_dict = {}
        condition_value = {'period', 'evaluations', 'method'}
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:

                value: str = vertex_value[vertex_key].as_string()
                if value.isnumeric():
                    value: int = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value: float = float(value)
                if vertex_key in condition_value:
                    condition_dict[vertex_key] = value
                else:
                    tmp_result[vertex_key] = value
        edges = set(trigger_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'event_filter':
                tmp_result['target_filter'] = construct_event_filter_definition(destination)
            elif edge == 'constraint':
                condition_clause = construct_condition_clause_definition(destination)
                if condition_clause.get('constraint'):
                    condition_dict['constraint'] = condition_clause.get('constraint')
                elif condition_clause.get('condition'):
                    if condition_dict != {}:
                        abort(500)
                    tmp_result['condition'] = condition_clause.get('condition')
            elif edge == 'action':
                tmp_result['action'] = construct_activity_definition(destination)
            else:
                print(edge)
                abort(500)
        if condition_dict != {}:
            tmp_result['condition'] = condition_dict
        result[vertex_value['name'].as_string()] = tmp_result

    return result
