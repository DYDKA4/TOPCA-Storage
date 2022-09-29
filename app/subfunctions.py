import yaml
from flask import jsonify

from nebula_communication.nebula_functions import find_vertex_by_properties, find_path
from nebula_communication.search.search_dependencies import find_dependencies_for_vertex
from nebula_communication.template_builder.type.ArtifactType import construct_artifact_type
from nebula_communication.template_builder.type.CapabilityType import construct_capability_type
from nebula_communication.template_builder.type.DataTypes import construct_data_type
from nebula_communication.template_builder.type.GroupType import construct_group_type
from nebula_communication.template_builder.type.InterfaceType import construct_interface_type
from nebula_communication.template_builder.type.NodeTypes import construct_node_type
from nebula_communication.template_builder.type.PolicyType import construct_policy_type
from nebula_communication.template_builder.type.RelationshipType import construct_relationship_type


def find_all_dependencies(cluster_name, node_type, node_name):
    template_builder = {
        'ArtifactType': (construct_artifact_type, 'artifact_types'),
        'CapabilityType': (construct_capability_type, 'capability_types'),
        'DataType': (construct_data_type, 'data_types'),
        'GroupType': (construct_group_type, 'group_types'),
        'InterfaceType': (construct_interface_type, 'interface_types'),
        'NodeType': (construct_node_type, 'node_types'),
        'PolicyType': (construct_policy_type, 'policy_types'),
        'RelationshipType': (construct_relationship_type, 'relationship_types')
    }
    vertexes = find_vertex_by_properties(node_type, name=node_name)
    if vertexes is None:
        return jsonify({'status': 200,
                        'result': None})
    result = find_path(str(vertexes.column_values('id'))[1:-1], f'"{cluster_name}"', type_path='REVERSELY')
    if len(result.column_values('p')) > 1:
        return jsonify({'status': 500,
                        'message': 'find two path from this node_name',
                        'result': None})
    if len(result.column_values('p')) < 1:
        return jsonify({'status': 400,
                        'message': 'find zero path from this node_name',
                        'result': None})
    vid = result.column_values('p')[0].as_path().start_node().get_id()
    print(vid)
    result = find_dependencies_for_vertex(vid)
    result[node_type].add(vid)
    answer = {}
    for vertex_type, set_of_vid in result.items():
        builder = template_builder.get(vertex_type)
        if builder:
            if vertex_type in {'RelationshipType', 'NodeType', 'InterfaceType'}:
                json_of_vid = builder[0](list_of_vid=list(set_of_vid), only=None)
            else:
                json_of_vid = builder[0](list_of_vid=list(set_of_vid))
            answer[builder[1]] = json_of_vid
    print(yaml.dump(answer, default_flow_style=False))

    return answer


# result = find_all_dependencies("TOSCA_DEFINITIONS_1", 'NodeType', "tosca.nodes.SoftwareComponent")