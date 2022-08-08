from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import go_from_over, complex_go_from_over_2dst_vertex_param, \
    go_from_over_dst_params
from nebula_communication.update_template.Other.MetadataUpdater import add_metadata, update_metadata


def is_service_status_exist(cluster_name, service_name):
    node_template = complex_go_from_over_2dst_vertex_param('"' + cluster_name + '"', 'topology_template',
                                                           'node_templates', service_name).column_values('id2')
    if len(node_template) > 1:
        abort(500)
    if node_template:
        node_template = node_template[0]
    # print(node_template)
    if go_from_over_dst_params(node_template, 'metadata', name='status').column_values('id'):
        return True
    return False


def add_service_status(cluster_name, service_name):
    node_template = complex_go_from_over_2dst_vertex_param('"' + cluster_name + '"', 'topology_template',
                                                           'node_templates', service_name).column_values('id2')
    if len(node_template) > 1:
        abort(500)
    if node_template:
        node_template = node_template[0]
    # print(node_template)
    add_metadata('add', ['', 'status'], '"busy"', 'value', cluster_name, node_template)
    return


def set_service_status(cluster_name, service_name, status='busy'):
    node_template = complex_go_from_over_2dst_vertex_param('"' + cluster_name + '"', 'topology_template',
                                                           'node_templates', service_name).column_values('id2')
    if len(node_template) > 1:
        abort(500)
    if node_template:
        node_template = node_template[0]
    update_metadata(node_template, f'"{status}"', 'value', ['metadata', 'status'], None)

