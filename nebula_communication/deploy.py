import yaml
import logging
import config
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

from random import choice
from string import ascii_uppercase

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.linker.LinkerValidTypes import link_valid_target_types
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition, \
    service_template_definition_parser

realised_vertex_type = {'ServiceTemplateDefinition', 'Metadata', 'RepositoryDefinition', 'ImportDefinition',
                        'ArtifactType', 'PropertyDefinition', 'ConstraintClause', 'SchemaDefinition', 'DataType',
                        'CapabilityType', 'AttributeDefinition', 'ArtifactDefinition', 'PropertyAssignments',
                        'OperationImplementationDefinition', 'OperationDefinition', 'InterfaceType', 'RelationshipType',
                        'InterfaceDefinition', 'NotificationDefinition', 'NotificationImplementationDefinition'}
realised_edge_type = {'metadata', 'repositories', 'imports', 'artifact_types', 'derived_from', 'properties',
                      'constraints', 'key_schema', 'entry_schema', 'data_types', 'capability_types', 'attributes'}
Config = Config()
Config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
ok = connection_pool.init([('10.100.151.128', 9669)], Config)


def start_session():
    session = connection_pool.get_session('Administator', 'password')
    result = session.execute(f'USE {config.WorkSpace}')
    assert result.is_succeeded(), result.error_msg()
    return session


def number_of_entities(session, vertex_name):
    # return of new index of new entities
    result = session.execute(f'LOOKUP ON {vertex_name}')
    print(f'LOOKUP ON {vertex_name}')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')
    if result:
        amount = 0
        for index in result:
            index = index.as_string()
            if int(index[len(vertex_name):]) > amount:
                amount = int(index[len(vertex_name):])
        return amount + 1
    else:
        return 1


def vid_getter(vertex_type):
    vertex_type = vertex_type
    session = start_session()
    vid = '"' + vertex_type + str(number_of_entities(session, vertex_type)) + '"'
    session.release()
    return vid


def add_in_vertex(vertex_name, name_of_key_value, key_value, vid):
    session = start_session()
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                             f':({key_value});')

    logging.info(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                 f':({key_value});')
    print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
          f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def add_edge(edge_name, edge_params, source_vertex, destination_vertex, data):
    session = start_session()
    result = session.execute(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    logging.info(f'INSERT EDGE {edge_name}({edge_params})'
                 f' VALUE {source_vertex}->{destination_vertex}:({data})')
    print(f'INSERT EDGE {edge_name}({edge_params})'
          f' VALUE {source_vertex}->{destination_vertex}:({data})')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def deploy(template) -> None:
    name_of_key_value = ''
    key_value = ''
    complex_vertex = {}
    for attribute_name, attribute_value in template.__dict__.items():
        if type(attribute_value) in {int, float, str, bool} and attribute_name not in {'vid', 'vertex_type_system'}:
            if name_of_key_value == '':
                if attribute_value is not None:
                    name_of_key_value = attribute_name
                    key_value = '"' + str(attribute_value) + '"'
            else:
                if attribute_value is not None:
                    name_of_key_value = name_of_key_value + ", " + attribute_name
                    key_value = key_value + ', "' + str(attribute_value) + '"'
        elif attribute_name not in {'vid', 'vertex_type_system'} and attribute_value is not None:
            complex_vertex[attribute_name] = attribute_value
    if template.vid is None:
        template.vid = vid_getter(template.vertex_type_system)
    # for edge in edges:
    #     add_edge(edge[0], edge[1], edge[2].vid, edge[3].vid, edge[4]) # todo Thing about it
    add_in_vertex(template.vertex_type_system, name_of_key_value, key_value, template.vid)
    for attribute_name, attribute_value in complex_vertex.items():
        if type(attribute_value) == list:
            for attribute_item in attribute_value:
                if attribute_item.vertex_type_system in realised_vertex_type:  # todo Remove when it will be done
                    deploy(attribute_item)
                    # edges.append([attribute_name, '', template, attribute_item, ''])
                    add_edge(attribute_name, '', template.vid, attribute_item.vid, '')
        elif type(attribute_value) == dict:
            for type_edge, vertexes in attribute_value.items():
                # edges.append([type_edge, '', vertexes[0], vertexes[1], ''])
                if type(vertexes[1]) == list:
                    for vertex in vertexes[1]:
                        add_edge(type_edge, '', vertexes[0].vid, vertex.vid, '')
                else:
                    add_edge(type_edge, '', vertexes[0].vid, vertexes[1].vid, '')
        else:
            if type(attribute_value) == bool:
                print(complex_vertex)
            if attribute_value.vertex_type_system in realised_vertex_type:  # todo Remove when it will be done
                deploy(attribute_value)
                # edges.append([attribute_name, '', template, attribute_value, ''])
                add_edge(attribute_name, '', template.vid, attribute_value.vid, '')

        print(attribute_name)
    return


file = open('service_template.yaml')
data = file.read()
file.close()
data = yaml.safe_load(data)
template = service_template_definition_parser(''.join(choice(ascii_uppercase) for i in range(12)), data)
for artifact_type in template.artifact_types:
    link_derived_from(template.artifact_types, artifact_type)
for data_type in template.data_types:
    link_derived_from(template.data_types, data_type)
for capability_type in template.capability_types:
    link_derived_from(template.capability_types, capability_type)
for interface_type in template.interface_types:
    link_derived_from(template.interface_types, interface_type)
for relationship_type in template.relationship_types:
    link_derived_from(template.relationship_types, relationship_type)
    link_valid_target_types(template.capability_types, relationship_type)
deploy(template)
