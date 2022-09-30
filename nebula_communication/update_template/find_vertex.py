import inspect

from nebula_communication.nebula_functions import get_all_vertex, fetch_vertex
from nebula_communication.redis_communication import get_all_vid_from_cluster
from nebula_communication.update_template import NebulaCommunicationUpdateTemplateException
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
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: vertex_type_system is None')
    elif search_by and search_by_value is None:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: search_by is not None '
                                                              f'and search_by_value is None')
    elif search_by is None and search_by_value:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: search_by is None '
                                                              f'and search_by_value not is None')
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
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: wrong arguments')
    return result
