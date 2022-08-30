from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment

from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.TriggerDefinition import construct_trigger_definition
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition


def construct_policy_definition(list_of_vid, only) -> list:
    result = []
    policy_type = PolicyDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'PolicyDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(policy_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                derived_from = fetch_vertex(destination[0], 'PolicyType')
                derived_from = derived_from.as_map()
                derived_from = derived_from['name'].as_string()
                tmp_result['type'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_assignment(destination, only)
            elif edge == 'targets':
                targets = []
                for target in destination:
                    if fetch_vertex(target, 'NodeTemplate'):
                        target = fetch_vertex(target, 'NodeTemplate')
                    elif fetch_vertex(target, 'GroupType'):
                        target = fetch_vertex(target, 'GroupType')
                    else:
                        abort(500)
                    target = target.as_map()
                    target = target['name'].as_string()
                    targets.append(target)
                tmp_result['targets'] = targets
            elif edge == 'triggers':
                tmp_result['triggers'] = construct_trigger_definition(destination)
            else:
                print(edge)
                abort(500)
        result.append({vertex_value['name'].as_string(): tmp_result})

    return result
