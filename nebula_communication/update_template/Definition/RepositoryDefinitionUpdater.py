from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_vertex, \
    add_in_vertex, add_edge
from parser.parser.tosca_v_1_3.definitions.RepositoryDefinition import RepositoryDefinition


def start_repository_definition(father_node_vid, varargs):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    repository_vid_to_update = None
    for repository_vid in destination:
        metadata_value = fetch_vertex(repository_vid, 'RepositoryDefinition')
        metadata_value = metadata_value.as_map()
        if metadata_value.get('name').as_string() == varargs[1]:
            repository_vid_to_update = repository_vid
            break
    if repository_vid_to_update is None:
        abort(400)
    return repository_vid_to_update


def update_repository_definition(father_node_vid, value, value_name, varargs: list, type_update):
    repository_vid_to_update = start_repository_definition(father_node_vid, varargs)
    if type_update == 'delete':
        delete_vertex('"' + repository_vid_to_update.as_string() + '"')
        return
    vertex_value = fetch_vertex(repository_vid_to_update, 'RepositoryDefinition')
    vertex_value = vertex_value.as_map()
    if value_name not in vertex_value.keys():
        abort(400)
    update_vertex('RepositoryDefinition', repository_vid_to_update, value_name, value)


def add_repository(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add':
        repository = RepositoryDefinition('"' + varargs[1] + '"')
        generate_uuid(repository, cluster_name)
        add_in_vertex(repository.vertex_type_system, 'name, vertex_type_system',
                      repository.name + ',"' + repository.vertex_type_system + '"', repository.vid)
        add_edge(edge_name, '', parent_vid, repository.vid, '')
        return True
    return False


def get_repository_definition(father_node_vid, value, value_name, varargs: list):
    repository_vid_to_update = start_repository_definition(father_node_vid, varargs)
    property_value = fetch_vertex(repository_vid_to_update, 'RepositoryDefinition')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        if value == property_value.get(value_name).as_string():
            return repository_vid_to_update.as_string()
    else:
        abort(400)
