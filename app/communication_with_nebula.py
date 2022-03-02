# define a Config
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config
import config
from app import data_classes

Config = Config()
Config.max_connection_pool_size = 10
# init connection pool
connection_pool = ConnectionPool()
# if the given servers are ok, return true, else return false
ok = connection_pool.init([(config.IP_address, 9669)], Config)


def hello_world():
    print('hello world')


def chose_of_space():
    # chose of working space session is still open
    session = connection_pool.get_session(config.UserName, config.UserPassword)
    result = session.execute(f'USE {config.WorkSpace}')
    assert result.is_succeeded(), result.error_msg()
    return session


def number_of_entities(session, vertex_name):
    # return of new index of new entities
    result = session.execute(f'LOOKUP ON {vertex_name}')
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


def is_unique_vid(session, vertex_name, vid):
    # return true if unique else false
    result = session.execute(f'LOOKUP ON {vertex_name}')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')
    # print(result)
    if result:
        for index in result:
            if index.as_string() == vid[1:-1]:
                return False
    return True


def add_in_vertex(session, vertex_name, name_of_key_value, key_value, vid):
    # add into vertex value
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                             f':({key_value});')
    print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
          f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    return


def add_edge(session, edge_name, edge_params, source_vertex, destination_vertex, data):
    result = session.execute(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    print(f'INSERT EDGE {edge_name}({edge_params})'
          f' VALUE {source_vertex}->{destination_vertex}:({data})')
    assert result.is_succeeded(), result.error_msg()
    return



def yaml_deploy(cluster_vertex: data_classes.ClusterName):
    """ программа за четыре прохода создает шаблон в бд,
    за первый проход она размещается все узлы в бд, за второй создаёт соотвествующие связи
    """
    session = chose_of_space()
    if not (is_unique_vid(session, cluster_vertex.vertex_type_system, cluster_vertex.vid)):
        return '400 Cluster VID is not unique'
    print(type(cluster_vertex.pure_yaml))
    assignment_vertex: data_classes.AssignmentVertex
    # добавление всех вершин связанных с definition vertex
    for assignment_vertex in cluster_vertex.assignment_vertex:
        assignment_vertex.set_vid(session)
        add_in_vertex(session, assignment_vertex.vertex_type_system, 'name', '"' + assignment_vertex.name + '"',
                      assignment_vertex.vid)

        # добавление property и capability в БД и ребра между defenition_vertex и property_vertex
        property_vertex: data_classes.AssignmentProperties
        for property_vertex in assignment_vertex.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'assignment_property', '', assignment_vertex.vid, property_vertex.vid, '')

        capability_vertex: data_classes.AssignmentCapabilities
        for capability_vertex in assignment_vertex.capabilities:
            capability_vertex.set_vid(session)
            add_in_vertex(session, capability_vertex.vertex_type_system, 'name',
                          f'"{capability_vertex.name}"', capability_vertex.vid)
            add_edge(session, 'assignment_capability', '', assignment_vertex.vid, capability_vertex.vid, '')
            for property_vertex in capability_vertex.properties:
                property_vertex.set_vid(session)
                add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                              f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
                add_edge(session, 'assignment_property', '', capability_vertex.vid, property_vertex.vid, '')
    for assignment_vertex in cluster_vertex.assignment_vertex:
        for destination_vertex, type_link in assignment_vertex.requirements.items():
            add_edge(session, 'assignment_requirements', 'name', assignment_vertex.vid, destination_vertex.vid,
                     f'"{type_link}"')

    # обработка defenition части
    capability_vertex: data_classes.DefinitionCapabilities
    for capability_vertex in cluster_vertex.definition_capabilities:
        capability_vertex.set_vid(session)
        add_in_vertex(session, capability_vertex.vertex_type_system, 'vertex_type_tosca',
                      f'"{capability_vertex.vertex_type_tosca}"', capability_vertex.vid)
        for property_vertex in capability_vertex.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'definition_property', 'name', capability_vertex.vid, property_vertex.vid,
                     f'"{property_vertex.name}"')
    definition_vertex: data_classes.DefinitionVertex
    for definition_vertex in cluster_vertex.definition_vertex:
        definition_vertex.set_vid(session)
        print(definition_vertex)
        add_in_vertex(session, definition_vertex.vertex_type_system, 'vertex_type_tosca',
                      f'"{definition_vertex.vertex_type_tosca}"', definition_vertex.vid)
        property_vertex: data_classes.DefinitionProperties
        for property_vertex in definition_vertex.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'definition_property', 'name', definition_vertex.vid, property_vertex.vid,
                     f'"{property_vertex.name}"')
        capability_vertex: data_classes.DefinitionCapabilities
        for capability_vertex in definition_vertex.capabilities:
            add_edge(session, 'definition_capability', '', definition_vertex.vid, capability_vertex.vid, '')

    add_in_vertex(session, cluster_vertex.vertex_type_system, 'pure_yaml', '"' + str(cluster_vertex.pure_yaml) + '"',
                  cluster_vertex.vid)

    for assignment_vertex in cluster_vertex.assignment_vertex:
        add_edge(session, 'assignment', '', cluster_vertex.vid, assignment_vertex.vid, '')
    for definition_vertex in cluster_vertex.definition_vertex:
        add_edge(session, 'definition', '', cluster_vertex.vid, definition_vertex.vid, '')
    # session.release()
    return '200 OK'
