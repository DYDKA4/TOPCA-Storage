import yaml
from nebula3.data.DataObject import ValueWrapper
from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import get_all_vertex, go_from_over, \
    complex_go_from_over_2dst_vertex_param, complex_go_from_over_1dst_vertex_param, go_from_over_dst_params
from nebula_communication.redis_communication import get_cluster_name_from_redis
from nebula_communication.search import NebulaCommunicationSearchException


def find_in_target_list(target_vid, result):
    result_node = complex_go_from_over_1dst_vertex_param(target_vid, 'requirements',
                                                         'node', 'host').column_values('id2')
    for result_node_vid in result_node:
        property_values = complex_go_from_over_1dst_vertex_param(result_node_vid, 'capabilities', 'properties',
                                                                 'endpoint')
        answer = {}
        for vid, props in zip(property_values.column_values("id2"), property_values.column_values("props")):
            props: ValueWrapper
            vid: ValueWrapper
            tmp_dict = {}
            for key, value in props.as_map().items():
                tmp_dict[key] = value.as_string()
            answer[vid.as_string()] = tmp_dict
        result[get_cluster_name_from_redis(result_node_vid.as_string())] = answer


def search_of_endpoint_from_son(type_of_template, cluster_name=None, find_free=None):
    result = {}
    target_list = []
    if cluster_name is None:
        cluster_names = get_all_vertex("ServiceTemplateDefinition")
        for cluster_vid in cluster_names:
            topology_template = go_from_over(cluster_vid, 'topology_template').column_values('id')
            if len(topology_template) > 1:
                raise NebulaCommunicationSearchException(500, 'topology_template len > 1')
            if topology_template:
                topology_template = topology_template[0]
                target_vid = complex_go_from_over_2dst_vertex_param(topology_template, "node_templates",
                                                                    "type", type_of_template).column_values('id')
                target_list += target_vid
    else:
        topology_template = go_from_over('"' + cluster_name + '"', 'topology_template').column_values('id')
        if len(topology_template) > 1:
            raise NebulaCommunicationSearchException(500, 'topology_template len > 1')
        if topology_template:
            topology_template = topology_template[0]
            target_vid = complex_go_from_over_2dst_vertex_param(topology_template, "node_templates",
                                                                "type", type_of_template).column_values('id')
            target_list += target_vid
    for target_vid in target_list:
        if find_free and go_from_over_dst_params(target_vid, 'metadata',
                                                 name='status', values='free').column_values('id'):
            find_in_target_list(target_vid, result)
        elif not find_free:
            find_in_target_list(target_vid, result)
    return result

# result = search_of_endpoint_from_son('michman.nodes.Jupyter.Jupyter-6-0-1', find_free=True)
# print(yaml.dump(result, default_flow_style=False))
