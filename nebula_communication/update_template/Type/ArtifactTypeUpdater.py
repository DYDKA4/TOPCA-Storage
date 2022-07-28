from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import form_result, return_all
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition, get_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType


def start_artifact_type(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    artifact_vid_to_update = None
    for artifact_vid in destination:
        artifact_value = fetch_vertex(artifact_vid, 'ArtifactType')
        artifact_value = artifact_value.as_map()
        if artifact_value.get('name').as_string() == varargs[1]:
            artifact_vid_to_update = artifact_vid
            break
    if artifact_vid_to_update is None:
        abort(400)
    return artifact_vid_to_update


def update_artifact_type(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
    artifact_vid_to_update = start_artifact_type(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + artifact_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(artifact_vid_to_update, 'ArtifactType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(artifact_vid_to_update, value_name)
            new_derived_artifact_vid = None
            for artifact_vid in destination:
                artifact_value = fetch_vertex(artifact_vid, 'ArtifactType')
                artifact_value = artifact_value.as_map()
                if '"' + artifact_value.get('name').as_string() + '"' == value:
                    new_derived_artifact_vid = artifact_vid
                    break
            if new_derived_artifact_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, artifact_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', artifact_vid_to_update, new_derived_artifact_vid, '')

        elif value_name in vertex_value.keys():
            update_vertex('ArtifactType', artifact_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        if not add_property_definition(type_update, varargs[2:], cluster_name, artifact_vid_to_update, varargs[2]):
            update_property_definition(father_node_vid, artifact_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, artifact_vid_to_update):
            update_metadata(artifact_vid_to_update, value, value_name, varargs[2:], type_update)
    else:
        abort(400)


def add_artifact_type(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        import_definition = ArtifactType('"' + varargs[1] + '"')
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'name, vertex_type_system',
                      import_definition.name + ',"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False


def get_artifact_type(father_node_vid, value, value_name, varargs: list):
    artifact_vid_to_update = start_artifact_type(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(artifact_vid_to_update, 'ArtifactType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            return form_result(artifact_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return artifact_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        destination = find_destination(artifact_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_metadata(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        destination = find_destination(artifact_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
