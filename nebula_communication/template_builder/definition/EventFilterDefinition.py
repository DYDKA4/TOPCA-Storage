from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from parser.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition


def construct_event_filter_definition(list_of_vid) -> dict:
    result = {}
    event_filter_definition = EventFilterDefinition('name').__dict__

    for vid in list_of_vid:
        node_type_flag = False
        vertex_value = fetch_vertex(vid, 'EventFilterDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        edge = 'node'
        vertex_keys = vertex_value.keys()
        edges = set(event_filter_definition.keys()) - set(vertex_keys) - {'vid'} - {edge}
        destination = find_destination(vid, edge)
        if fetch_vertex(destination[0], 'NodeType'):
            node = fetch_vertex(destination[0], 'NodeType')
            node_type_flag = True
        elif fetch_vertex(destination[0], 'NodeTemplate'):
            node = fetch_vertex(destination[0], 'NodeTemplate')
        else:
            abort(500)
        node = node.as_map()
        node = node['name'].as_string()
        tmp_result['node'] = node
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'requirement':
                if destination:
                    if node_type_flag:
                        requirement = fetch_vertex(destination[0], 'RequirementDefinition')
                        requirement = requirement.as_map()
                        requirement = requirement['name'].as_string()
                        if requirement is None:
                            abort(500)
                    else:
                        requirement = fetch_vertex(destination[0], 'RequirementAssignment')
                        if requirement is None:
                            abort(500)
                        requirement = requirement.as_map()
                        requirement = requirement['name'].as_string()
                    tmp_result['requirement'] = requirement
            elif edge == 'capability':
                if destination:
                    if node_type_flag:
                        capability = fetch_vertex(destination[0], 'CapabilityDefinition')
                        if capability is None:
                            abort(500)
                        capability = capability.as_map()
                        capability = capability['name'].as_string()
                    else:
                        capability = fetch_vertex(destination[0], 'CapabilityAssignment')
                        if capability is None:
                            abort(500)
                        capability = capability.as_map()
                        capability = capability['name'].as_string()
                    tmp_result['capability'] = capability
            else:
                abort(500)
        result = tmp_result

    return result
