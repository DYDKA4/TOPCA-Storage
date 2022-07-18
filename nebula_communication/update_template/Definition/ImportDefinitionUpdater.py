from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_vertex, \
    add_in_vertex, add_edge
from parser.parser.tosca_v_1_3.definitions.ImportDefinition import ImportDefinition


def update_import_definition(father_node_vid, value, value_name, varargs: list, type_update):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    repository_vid_to_update = None
    for repository_vid in destination:
        metadata_value = fetch_vertex(repository_vid, 'ImportDefinition')
        metadata_value = metadata_value.as_map()
        if metadata_value.get('file').as_string() == varargs[1]:
            repository_vid_to_update = repository_vid
            break
    if repository_vid_to_update is None:
        abort(400)
    vertex_value = fetch_vertex(repository_vid_to_update, 'ImportDefinition')
    vertex_value = vertex_value.as_map()
    if value_name not in vertex_value.keys():
        abort(400)
    update_vertex('ImportDefinition', repository_vid_to_update, value_name, value)


def add_import_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add':
        import_definition = ImportDefinition()
        import_definition.file = '"' + varargs[1] + '"'
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'file, vertex_type_system',
                      import_definition.file + ',"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False
