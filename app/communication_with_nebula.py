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


def is_updated(session, vertex_name):
    result = session.execute(f'LOOKUP ON {vertex_name}')
    while not result.is_succeeded():
        print(result.is_succeeded(), result.error_msg(), vertex_name)
        result = session.execute(f'LOOKUP ON {vertex_name}')
        session.release()
        session = chose_of_space()
    return session


def is_already_recorded(session, vertex_name, name_of_key_value, key_value):
    # return is this already recorded
    result = session.execute(f'LOOKUP ON {vertex_name} WHERE {vertex_name}.{name_of_key_value} == "{key_value}";')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')
    if result:
        result = result[0]
    return result


def create_vertex_if_nox_exist(session, type_of_node, attributes):
    result = session.execute(f'CREATE TAG IF NOT EXISTS {type_of_node} (name fixed_string(256) NOT NULL)')
    print(f'CREATE TAG IF NOT EXISTS {type_of_node} (name fixed_string(256) NOT NULL)')
    assert result.is_succeeded(), result.error_msg()
    if attributes:
        for attribute in attributes:
            result = session.execute(f'ALTER TAG {type_of_node} ADD ({attribute} fixed_string(256) NULL)')
            if result.is_succeeded() or result.error_msg() != 'Existed!':
                assert result.is_succeeded(), result.error_msg()
    result = session.execute(f'CREATE TAG INDEX IF NOT EXISTS Index_{type_of_node} on {type_of_node}(name)')
    assert result.is_succeeded(), result.error_msg()
    return


def add_in_vertex(session, vertex_name, name_of_key_value, key_value, vid):
    # add into vertex value
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                             f':({key_value});')
    print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
          f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    return


def create_edge_if_nox_exist(session, type_of_link):
    result = session.execute(f'CREATE EDGE IF NOT EXISTS {type_of_link} ()')
    # print(f'CREATE TAG IF NOT EXISTS {type_of_link} ()')
    assert result.is_succeeded(), result.error_msg()
    result = session.execute(f'CREATE EDGE INDEX IF NOT EXISTS Index{type_of_link} on {type_of_link}()')
    # print(f'CREATE EDGE INDEX IF NOT EXISTS Index{type_of_link} on {type_of_link}()')
    assert result.is_succeeded(), result.error_msg()
    return


def add_edge(session, edge_name, edge_params, source_vertex, destination_vertex, data):
    result = session.execute(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    print(f'INSERT EDGE {edge_name}({edge_params})'
          f' VALUE {source_vertex}->{destination_vertex}:({data})')
    assert result.is_succeeded(), result.error_msg()
    return


def add_server(cpu, ram, mem, owner, date):
    session = chose_of_space()
    # search for an existing user
    is_recorded = is_already_recorded(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner)
    if not is_recorded:
        source_vertex = number_of_entities(session, config.NameOfUserVertex)
        owner = '"' + owner + '"'
        source_vertex = f'"{config.NameOfUserVertex}{source_vertex}"'
        add_in_vertex(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner, source_vertex)
    else:
        source_vertex = is_recorded
    destination_vertex = number_of_entities(session, config.NameOfServerVertex)
    destination_vertex = f'"{config.NameOfServerVertex}{destination_vertex}"'
    add_in_vertex(session, config.NameOfServerVertex, config.NameOfKeyValueServer, f'{cpu},{ram},{mem}',
                  destination_vertex)
    date = list(date)
    date[10] = 'T'
    date = "".join(date)
    date = f'datetime("{date}")'
    add_edge(session, config.NameOfOwnerEdge, config.NameOfKeyValueOwner, source_vertex, destination_vertex, date)

    session.release()


def find_server(cpu, ram, mem, owner):
    # return list of this servers with owner
    session = chose_of_space()
    owner = is_already_recorded(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner)
    if not owner:
        return 0
    assert owner, "such owner not existed"
    result = session.execute(f'GO FROM {owner} over owner'
                             f' WHERE properties($$).cpu == {cpu} AND properties($$).ram == {ram} AND'
                             f' properties($$).mem == {mem} '
                             'YIELD properties($^).name as name, properties($$).cpu as cpu,'
                             ' properties($$).ram as ram, properties($$).mem as mem,'
                             ' properties(edge).date_of_creation as date_of_creation')

    assert result.is_succeeded(), result.error_msg()
    answer = []
    for key in result.keys():

        tmp_answer = []
        if not result.column_values(key):
            return 0
        for value in result.column_values(key):
            if value.is_int():
                tmp_answer += [{
                    f'{key}': value.as_int()}]
            elif value.is_string():
                tmp_answer += [{
                    f'{key}': value.as_string()}]
            elif value.is_datetime():
                tmp_answer += [{
                    'year': value.as_datetime().get_year(),
                    'month': value.as_datetime().get_month(),
                    'day': value.as_datetime().get_day(),
                    'hour': value.as_datetime().get_hour(),
                    'minute': value.as_datetime().get_minute(),
                    'sec': value.as_datetime().get_sec(),
                    'microsecond': value.as_datetime().get_microsec()}]
        answer += [tmp_answer]

    session.release()
    return answer


def name_to_index(rename, data):
    for node in data:
        node[0] = rename[node[0]]
        if len(node) > 2:
            # print(node)
            if type(node[2]) == list and node[2][0]:
                for link in node[2]:
                    # print(link)
                    link[1] = rename[link[1]]
    return data


def get_attributes_name(data):
    result = []
    if data[0]:
        for frame in data:
            result += [frame[0]]
    return result


def get_attributes(data):
    result = []
    if data[0]:
        for frame in data:
            result += [frame[1]]
    return result


def form_name_key_value(data):
    res = ''
    for name in data:
        res += name + ', '
    res = res[:-2]
    return res


def form_key_value(data):
    result = ''
    for key in data:
        result += '"' + str(key) + '"' + ', '
    result = result[:-2]
    return result


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
            capability_vertex.set_vid(session)
            add_in_vertex(session, capability_vertex.vertex_type_system, 'vertex_type_tosca',
                          f'"{capability_vertex.vertex_type_tosca}"', capability_vertex.vid)
            add_edge(session, 'definition_capability', '', definition_vertex.vid, capability_vertex.vid, '')
            for property_vertex in capability_vertex.properties:
                property_vertex.set_vid(session)
                add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                              f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
                add_edge(session, 'definition_property', 'name', capability_vertex.vid, property_vertex.vid,
                         f'"{property_vertex.name}"')

    add_in_vertex(session, cluster_vertex.vertex_type_system, 'pure_yaml', '"' + str(cluster_vertex.pure_yaml) + '"',
                  cluster_vertex.vid)

    for assignment_vertex in cluster_vertex.assignment_vertex:
        add_edge(session, 'assignment', '', cluster_vertex.vid, assignment_vertex.vid, '')
    for definition_vertex in cluster_vertex.definition_vertex:
        add_edge(session, 'definition', '', cluster_vertex.vid, definition_vertex.vid, '')
    # session.release()
    return '200 OK'
