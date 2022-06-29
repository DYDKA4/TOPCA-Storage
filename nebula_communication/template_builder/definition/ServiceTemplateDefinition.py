import yaml
from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.ImportDefinition import construct_import_definition
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.RepositoryDefinition import construct_repository_definition
from nebula_communication.template_builder.type.ArtifactType import construct_artifact_type
from nebula_communication.template_builder.type.CapabilityType import construct_capability_type
from nebula_communication.template_builder.type.DataTypes import construct_data_type
from nebula_communication.template_builder.type.GroupType import construct_group_type
from nebula_communication.template_builder.type.InterfaceType import construct_interface_type
from nebula_communication.template_builder.type.NodeTypes import construct_node_type
from nebula_communication.template_builder.type.PolicyType import construct_policy_type
from nebula_communication.template_builder.type.RelationshipType import construct_relationship_type
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def construct_service_template_definition(name: str):
    name = '"'+name + '"'
    vertex_value = fetch_vertex(name, 'ServiceTemplateDefinition')
    vertex_value = vertex_value.as_map()
    vertex_keys = vertex_value.keys()
    service_template_definition = ServiceTemplateDefinition('name').__dict__
    template = {}
    for vertex_key in vertex_keys:
        if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
            value = vertex_value[vertex_key].as_string()
            value: str
            if value.isnumeric():
                value: int = int(value)
            elif value.replace('.', '', 1).isdigit():
                value: float = float(value)
            template[vertex_key] = value
    edges = set(service_template_definition.keys()) - set(vertex_keys) - {'vid'}
    for edge in edges:
        destination = find_destination(name, edge)
        if destination:
            if edge == 'metadata':
                template['metadata'] = construct_metadata_definition(destination)
            elif edge == 'repositories':
                template['repositories'] = construct_repository_definition(destination)
            elif edge == 'imports':
                template['imports'] = construct_import_definition(destination)
            elif edge == 'artifact_types':
                template['artifact_types'] = construct_artifact_type(destination)
            elif edge == 'data_types':
                template['data_types'] = construct_data_type(destination)
            elif edge == 'capability_types':
                template['capability_types'] = construct_capability_type(destination)
            elif edge == 'interface_types':
                template['interface_types'] = construct_interface_type(destination)
            elif edge == 'relationship_types':
                template['relationship_types'] = construct_relationship_type(destination)
            elif edge == 'node_types':
                template['node_types'] = construct_node_type(destination)
            elif edge == 'group_types':
                template['group_types'] = construct_group_type(destination)
            elif edge == 'policy_types':
                template['policy_types'] = construct_policy_type(destination)
            elif edge == 'topology_template':
                print(edge, destination)
            else:
                abort(500)

    with open('./output.yaml', 'w') as file:
        documents = yaml.dump(template, file)


construct_service_template_definition('NUDEXHPAFTBW')
