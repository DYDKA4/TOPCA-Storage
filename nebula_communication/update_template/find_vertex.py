from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import get_all_vertex, fetch_vertex
from nebula_communication.redis_communication import get_all_vid_from_cluster
from nebula_communication.update_template.Definition.ImportDefinitionUpdater import get_import_definition
from nebula_communication.update_template.Definition.RepositoryDefinitionUpdater import get_repository_definition
from nebula_communication.update_template.Definition.TopologyTemplateDefinitionUpdater import \
    get_topology_template_definition
from nebula_communication.update_template.Other.MetadataUpdater import get_metadata
from nebula_communication.update_template.Type.ArtifactTypeUpdater import get_artifact_type
from nebula_communication.update_template.Type.CapabilityTypeUpdater import get_capability_type
from nebula_communication.update_template.Type.DataTypeUpdater import get_data_type
from nebula_communication.update_template.Type.GroupTypeUpdater import get_group_type
from nebula_communication.update_template.Type.InterfaceTypeUpdater import get_interface_type
from nebula_communication.update_template.Type.NodeTypeUpdater import get_node_type
from nebula_communication.update_template.Type.PolicyTypeUpdater import get_policy_type
from nebula_communication.update_template.Type.RelationshipTypeUpdater import get_relationship_type
from nebula_communication.update_template.find_functions import get_names, get_attribute, get_cluster_name


def find_vertex(cluster_name, vertex_type_system, search_by, search_by_value):
    if vertex_type_system is None:
        abort(400)
    elif search_by and search_by_value is None:
        abort(400)
    elif search_by is None and search_by_value:
        abort(400)
    if cluster_name is None:
        if search_by is None:
            vid = []
            vid_from_nebula = get_all_vertex(vertex_type_system)
            for vid_tmp in vid_from_nebula:
                vid.append(vid_tmp.as_string())
            return vid
        elif search_by and search_by_value:
            result = []
            vid_from_nebula = get_all_vertex(vertex_type_system)
            for vid in vid_from_nebula:
                vid_value = fetch_vertex(vid, vertex_type_system)
                vid_value = vid_value.as_map()
                if not vid_value.get(search_by).is_null():
                    if vid_value.get(search_by).as_string() == search_by_value:
                        result.append(vid.as_string())
            return result
    elif cluster_name:
        vid_from_nebula = get_all_vertex(vertex_type_system)
        vid = []
        for vid_tmp in vid_from_nebula:
            vid.append(vid_tmp.as_string())
        vid_from_cluster = get_all_vid_from_cluster(cluster_name)
        vid = list(set(vid) & set(vid_from_cluster))
        if search_by is None:
            return vid
        elif search_by and search_by_value:
            result = []
            for vid_tmp in vid:
                vid_value = fetch_vertex('"' + vid_tmp + '"', vertex_type_system)
                vid_value = vid_value.as_map()
                if not vid_value.get(search_by).is_null():
                    if vid_value.get(search_by).as_string() == search_by_value:
                        result.append(vid_tmp)
            return result
    vid = None
    #
    return vid


def find_template(cluster_name: str, value, value_name, vertex_type_system: str, varargs: list, ):
    result = None
    if not varargs:
        result = find_vertex(cluster_name, vertex_type_system, value_name, value)
        if result is not None:
            return result
    cluster_vid = '"' + cluster_name + '"'
    value = '"' + value + '"'
    if varargs[0] == 'metadata':  # todo Тестить
        result = get_metadata(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'repositories':  # todo Тестить
        result = get_repository_definition(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'imports':  # todo Тестить
        result = get_import_definition(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'artifact_types':  # todo Тестить
        result = get_artifact_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'data_types':  # todo Тестить
        result = get_data_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'capability_types':  # todo Тестить
        result = get_capability_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'interface_types':  # todo Тестить
        result = get_interface_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'relationship_types':  # todo Тестить
        result = get_relationship_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'node_types':  # todo Тестить
        result = get_node_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'group_types':  # todo Тестить
        result = get_group_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'policy_types':  # todo Тестить
        result = get_policy_type(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'topology_template':  # todo Тестить
        result = get_topology_template_definition(cluster_vid, value, value_name, varargs)
    else:
        abort(400)
    return result


# res = find_template('Jupyter_0', None, None, 'NodeTemplate',
#                     [])
# # res = find_template('Jupyter_0', 'michman.nodes.Jupyter.Jupyter-6-0-1', 'type', 'NodeTemplate',
# #                     ['topology_template', 'node_templates', 'jupyter_1'])
# res = get_names(res, 'NodeTemplate')
# res_type = find_template('Jupyter_0', 'michman.nodes.Jupyter.Jupyter-6-0-1', 'name', 'NodeType',
#                          [])[0]
# print(res_type)
# print(res)
# source_name = ''
# for uuid, name in res.items():
#     res_type_new = find_template('Jupyter_0', 'does not meter', 'type', 'NodeTemplate',
#                                  ['topology_template', 'node_templates', name])
#     # print(res_type_new, res_type)
#     if res_type_new == res_type:
#         print(name, uuid)
#         source_name = name
#         break
# res = find_template('Jupyter_0', 'does not meter', 'node', 'NodeTemplate',
#                                  ['topology_template', 'node_templates', source_name, 'requirements', 'host'])
# res = get_attribute(res, 'NodeTemplate', 'name')
# res = find_template('Jupyter_0', 'does not meter', '', 'NodeTemplate',
#                     ['topology_template', 'node_templates', res, 'capabilities', 'endpoint', 'properties', 'port'])
# print(res)
# print(get_attribute(res, 'PropertyAssignment', 'value'))




# res = find_template(None, None, None, 'NodeTemplate',
#                     [])
#
# cluster_name = get_cluster_name(res)
# res = get_names(res, 'NodeTemplate')
#
# for cluster in list(set(cluster_name.values())):
#     res_type = find_template(cluster, 'michman.nodes.Jupyter.Jupyter-6-0-1', 'name', 'NodeType',
#                              [])
#     result = None
#     if res_type:
#         res_type = res_type[0]
#         source_name = ''
#         res_type_new = None
#         for uuid, name in res.items():
#             res_type_new = find_template(cluster, 'does not meter', 'type', 'NodeTemplate',
#                                          ['topology_template', 'node_templates', name])
#             if res_type_new == res_type:
#                 source_name = name
#                 break
#         if res_type_new:
#             result = find_template(cluster, 'does not meter', 'node', 'NodeTemplate',
#                                    ['topology_template', 'node_templates', source_name, 'requirements', 'host'])
#             result = get_attribute(result, 'NodeTemplate', 'name')
#             result = find_template(cluster, 'does not meter', '', 'NodeTemplate',
#                                    ['topology_template', 'node_templates', result, 'capabilities', 'endpoint',
#                                     'properties',
#                                     'port'])
#     print(result)
