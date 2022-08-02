from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.find_functions import form_result
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition


def start_artifact_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    artifact_vid_to_update = None
    for artifact_vid in destination:
        artifact_value = fetch_vertex(artifact_vid, 'ArtifactDefinition')
        artifact_value = artifact_value.as_map()
        if artifact_value.get('name').as_string() == varargs[1]:
            artifact_vid_to_update = artifact_vid
            break
    if artifact_vid_to_update is None:
        abort(400)
    return artifact_vid_to_update

def update_artifact_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                               type_update):
    artifact_vid_to_update = start_artifact_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + artifact_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(artifact_vid_to_update, 'ArtifactDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(artifact_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'artifact_types')
            for artifact_type_vid in destination:
                artifact_type_value = fetch_vertex(artifact_type_vid, 'ArtifactType')
                artifact_type_value = artifact_type_value.as_map()
                if '"' + artifact_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = artifact_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, artifact_vid_to_update, type_vertex[0])
            add_edge(value_name, '', artifact_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('ArtifactDefinition', artifact_vid_to_update, value_name, value)
        else:
            abort(501)
    else:
        abort(400)


def add_artifact_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = ArtifactDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_artifact_definition(father_node_vid, value, value_name, varargs: list):
    artifact_vid_to_update = start_artifact_definition(father_node_vid, varargs)
    artifact_value = fetch_vertex(artifact_vid_to_update, 'ArtifactDefinition')
    artifact_value = artifact_value.as_map()
    if value_name == 'type':
        return form_result(artifact_vid_to_update, value_name)
    if value_name in artifact_value.keys():
        if value == artifact_value.get(value_name).as_string():
            return artifact_vid_to_update.as_string()
    else:
        abort(400)
