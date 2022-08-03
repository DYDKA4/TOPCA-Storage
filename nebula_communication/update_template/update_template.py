from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import update_vertex, fetch_vertex, add_in_vertex, add_edge
from nebula_communication.update_template.Definition.ImportDefinitionUpdater import update_import_definition, \
    add_import_definition
from nebula_communication.update_template.Definition.RepositoryDefinitionUpdater import update_repository_definition, \
    add_repository
from nebula_communication.update_template.Definition.TopologyTemplateDefinitionUpdater import \
    update_topology_template_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata
from nebula_communication.update_template.Type.ArtifactTypeUpdater import update_artifact_type, add_artifact_type
from nebula_communication.update_template.Type.CapabilityTypeUpdater import update_capability_type, add_capability_type
from nebula_communication.update_template.Type.DataTypeUpdater import update_data_type, add_data_type
from nebula_communication.update_template.Type.GroupTypeUpdater import update_group_type, add_group_type
from nebula_communication.update_template.Type.InterfaceTypeUpdater import update_interface_type, add_interface_type
from nebula_communication.update_template.Type.NodeTypeUpdater import update_node_type, add_node_type
from nebula_communication.update_template.Type.PolicyTypeUpdater import update_policy_type, add_policy_type
from nebula_communication.update_template.Type.RelationshipTypeUpdater import update_relationship_type, \
    add_relationship_type
from parser.parser.tosca_v_1_3.others.Metadata import Metadata


def update_template(cluster_name: str, value, value_name, varargs: list, type_update):
    cluster_vid = '"' + cluster_name + '"'
    value = '"' + value + '"'
    if len(varargs) == 0:
        vertex_value = fetch_vertex(cluster_vid, 'ServiceTemplateDefinition')
        vertex_value = vertex_value.as_map()
        if value_name not in vertex_value.keys() or type_update is not None:
            abort(400)
        update_vertex('ServiceTemplateDefinition', cluster_vid, value_name, value)
    elif varargs[0] == 'metadata':
        if not add_metadata(type_update, varargs, value, value_name, cluster_name, cluster_vid):
            update_metadata(cluster_vid, value, value_name, varargs, type_update)
    elif varargs[0] == 'repositories':
        if not add_repository(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_repository_definition(cluster_vid, value, value_name, varargs, type_update)
    elif varargs[0] == 'imports':
        if not add_import_definition(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_import_definition(cluster_vid, value, value_name, varargs, type_update)
    elif varargs[0] == 'artifact_types':
        if not add_artifact_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_artifact_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'data_types':
        if not add_data_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_data_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'capability_types':
        if not add_capability_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_capability_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'interface_types':  # todo Тестить
        if not add_interface_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_interface_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'relationship_types':  # todo Тестить
        if not add_relationship_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_relationship_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'node_types':  # todo Тестить
        if not add_node_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_node_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'group_types':  # todo Тестить
        if not add_group_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_group_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'policy_types':  # todo Тестить
        if not add_policy_type(type_update, varargs, cluster_name, cluster_vid, varargs[0]):
            update_policy_type(cluster_vid, value, value_name, varargs, type_update, cluster_name)
    elif varargs[0] == 'topology_template':  # todo Тестить
        update_topology_template_definition(cluster_vid, value, value_name, varargs)
    else:
        abort(400)


# update_template('cluster', 'new_key_value_2', 'value', ['artifact_types', 'test_parent_artifact_type_name',
#                                                              'properties', 'test_property_name_1', 'key_schema',
#                                                              'key_schema', 'constraints', 'key_equal_2'])
#
# update_template('SSNLEHCCGKGF', 'test_node_type_name_0', 'valid_source_types',
#                 ['capability_types', 'test_capability_type_name_0',
#                  ])

# update_template('SSNLEHCCGKGF', 'new_metadata_value', 'value',
#                 ['artifact_types', 'new_artifact_type', 'properties', 'new_property_definition'], 'delete')

# update_template('SSNLEHCCGKGF', 'new_metadata_value', 'value',
#                 ['artifact_types', 'new_artifact_type', 'properties', 'new_property_definition', 'key_schema',
#                  'key_schema'], 'add')

# update_template('SSNLEHCCGKGF', 'new_metadata_value', 'value',
#                 ['capability_types', 'new_capability_type'], 'delete')
