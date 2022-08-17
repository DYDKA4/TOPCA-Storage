import yaml
from flask import abort
from nebula2.fbthrift.util.randomizer import deep_dict_update

from nebula_communication.nebula_functions import find_vertex_by_properties, go_from_over, fetch_vertex, find_path
from nebula_communication.redis_communication import get_cluster_name_from_redis


def find_node_template_of_property(cluster_name=None, **parameters):
    answer = {}
    exit_answer = {}
    result = find_vertex_by_properties("PropertyAssignment", **parameters).column_values('id')
    if cluster_name is None:
        cluster_names = find_vertex_by_properties("ServiceTemplateDefinition").column_values('id')
    else:
        cluster_names = '["' + str(cluster_name) + '"]'
    result = find_path(str(cluster_names)[1:-1], str(result)[1:-1]).column_values('path')
    for path in result:
        path = path.as_path()
        for node_vid in path.nodes():
            data = fetch_vertex(node_vid.get_id(), 'NodeTemplate')
            if data:
                print(data)
                tmp_dict = {}
                answer = {}
                for key, value in data.as_map().items():
                    if value.is_string():
                        tmp_dict[key] = value.as_string()
                answer[node_vid.get_id().as_string()] = tmp_dict
        if answer:
            exit_answer[path.start_node().get_id().as_string()] = answer
    return exit_answer


# res = find_node_template_of_property()
# print(yaml.dump(res, default_flow_style=False))
