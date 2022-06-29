from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.AttributeAssignment import construct_attribute_assignment
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition


def construct_group_definition(list_of_vid) -> dict:
    result = {}
    group_type = GroupDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'GroupDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(group_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                derived_from = fetch_vertex(destination[0], 'GroupType')
                derived_from = derived_from.as_map()
                derived_from = derived_from['name'].as_string()
                tmp_result['type'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_assignment(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_assignment(destination)
            elif edge == 'members':  # todo only NodeTemplate support
                members = []
                for member in destination:
                    member = fetch_vertex(member, 'NodeTemplate')
                    member = member.as_map()
                    member = member['name'].as_string()
                    members.append(member)
                tmp_result['members'] = members
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
