import yaml

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
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
            template[vertex_key] = vertex_value[vertex_key].as_string()
    edges = set(service_template_definition.keys()) - set(vertex_keys) - {'vid'}
    for edge in edges:
        destination = find_destination(name, edge)
        if destination:
            if edge == 'metadata':
                template['metadata'] = construct_metadata_definition(destination)
                print(edge, destination)
            elif edge == 'repositories':
                print(edge, destination)
            elif edge == 'imports':
                print(edge, destination)
            elif edge == 'artifact_types':
                print(edge, destination)
            elif edge == 'data_types':
                print(edge, destination)
            elif edge == 'capability_types':
                print(edge, destination)
            elif edge == 'interface_types':
                print(edge, destination)
            elif edge == 'relationship_types':
                print(edge, destination)
            elif edge == 'node_types':
                print(edge, destination)
            elif edge == 'group_types':
                print(edge, destination)
            elif edge == 'policy_types':
                print(edge, destination)
            elif edge == 'topology_template':
                print(edge, destination)

    with open('./output.yaml', 'w') as file:
        documents = yaml.dump(template, file)


construct_service_template_definition('ZVMOLWFZMIGW')