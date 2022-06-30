from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.other.ConstraintClause import construct_constraint_schema

from parser.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import PropertyFilterDefinition


def construct_property_filter_definition(list_of_vid) -> list:
    result = []

    property_definition = PropertyFilterDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'PropertyFilterDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = []
        vertex_keys = vertex_value.keys()
        edges = set(property_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'property_constraint':
                tmp_result += construct_constraint_schema(destination)
            else:
                abort(500)
        result.append({vertex_value['name'].as_string(): tmp_result})
    return result
