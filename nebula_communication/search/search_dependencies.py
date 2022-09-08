from nebula3.data.DataObject import ValueWrapper

from nebula_communication.nebula_functions import find_all_edges


def find_dependencies_for_vertex(vid):
    result = {
        'ArtifactType': set(),
        'CapabilityType': set(),
        'DataType': set(),
        'GroupType': set(),
        'InterfaceType': set(),
        'NodeType': set(),
        'PolicyType': set(),
        'RelationshipType': set(),
        'Total_amount_of_vertex': set()
    }
    result_change = True
    old_amount_of_vertex = 0
    steps = 1
    while result_change:
        all_vid = find_all_edges(vid, steps)
        for vid_total in list(zip(all_vid.column_values('id'), all_vid.column_values('props'))):
            result['Total_amount_of_vertex'].add((vid_total[0],
                                                  vid_total[1].as_map().get('vertex_type_system').as_string()))
        result_change = old_amount_of_vertex != len(result['Total_amount_of_vertex'])
        old_amount_of_vertex = len(result['Total_amount_of_vertex'])
        steps += 1
    for vid, vertex_type_system in result['Total_amount_of_vertex']:
        if vertex_type_system in result.keys():
            result[vertex_type_system].add(vid)
    return result

#
# res = find_dependencies_for_vertex('"90f0bc82-41bd-43b2-83ad-16deb55252d5"')
# for ite, value in res.items():
#     print(ite, value)
