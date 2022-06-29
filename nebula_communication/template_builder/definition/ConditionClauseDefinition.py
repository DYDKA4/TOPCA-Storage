from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.AssertDefinition import construct_assert_definition
from parser.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import ConditionClauseDefinition


def construct_condition_clause_definition(list_of_vid) -> dict:
    result = {}

    condition_clause_definition = ConditionClauseDefinition('condition').__dict__
    if len(list_of_vid) > 1:
        abort(500)
    for vid in list_of_vid:
        tmp_result = []
        vertex_value = fetch_vertex(vid, 'ConditionClauseDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(condition_clause_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if destination:
                if edge == 'condition_not':
                    tmp_result += (construct_condition_clause_definition(destination))
                elif edge == 'condition_or':
                    tmp_result += (construct_condition_clause_definition(destination))
                elif edge == 'condition_and':
                    tmp_result += (construct_condition_clause_definition(destination))
                elif edge == 'condition_assert':
                    tmp_result += (construct_assert_definition(destination))
                else:
                    abort(500)
        result = {vertex_value['type'].as_string(): tmp_result}
    return result
