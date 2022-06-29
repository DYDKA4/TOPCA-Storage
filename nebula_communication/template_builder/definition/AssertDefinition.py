from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.SchemaDefinition import construct_schema_definition
from nebula_communication.template_builder.other.ConstraintClause import construct_constraint_schema
from parser.parser.tosca_v_1_3.definitions.AssertDefinition import AssertDefinition


def construct_assert_definition(list_of_vid) -> list:
    result = []

    assert_definition = AssertDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'AssertDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        edges = set(assert_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'constraint_clauses':
                tmp_result['attribute_name'] = construct_constraint_schema(destination)
            else:
                abort(500)
        result.append(tmp_result)
    return result
