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


def delete_all_edge(session, vertex, edge_name):
    result = session.execute(f'GO FROM {vertex} OVER {edge_name}\n'
                             f'YIELD src(edge) AS src, dst(edge) AS dst, rank(edge) AS rank'
                             f' | DELETE EDGE {edge_name} $-.src->$-.dst @ $-.rank;')
    print(f'GO FROM {vertex} OVER {edge_name}\n'
          f'YIELD src(edge) AS src, dst(edge) AS dst, rank(edge) AS rank'
          f' | DELETE EDGE {edge_name} $-.src->$-.dst @ $-.rank;')
    assert result.is_succeeded(), result.error_msg()
    return


def update_vertex(session, vertex_name, name_of_key_value, key_value, vid, start_session=False):
    if start_session:
        session = chose_of_space()
    update = 'UPDATE'
    result = session.execute(f'{update} VERTEX ON {vertex_name} {vid} set {name_of_key_value} = {key_value}')
    print(f'{update} VERTEX ON {vertex_name} {vid} set {name_of_key_value} = {key_value}')
    assert result.is_succeeded(), result.error_msg()
    if start_session:
        session.release()
    return


def get_yaml_from_cluster(cluster_name):
    session = chose_of_space()
    result = session.execute(f'FETCH PROP ON ClusterName "{cluster_name}"'
                             f' YIELD properties(vertex).pure_yaml AS pure_yaml;')
    print(f'FETCH PROP ON ClusterName "{cluster_name}"'
          f' YIELD properties(vertex).pure_yaml AS pure_yaml;')
    assert result.is_succeeded(), result.error_msg()
    if result.column_values('pure_yaml'):
        result = result.column_values('pure_yaml')[0].as_string()
    else:
        return None
    session.release()
    return result


def find_destination_by_property(session, vid, edge_name, property_name, property_value, start_session=False):
    if start_session:
        session = chose_of_space()
    result = session.execute(f'GO FROM {vid} over {edge_name} '
                             f'WHERE properties($$).{property_name} == "{property_value}"'
                             f' YIELD properties($$).{property_name} as {property_name}, dst(edge) as vid')
    print(f'GO FROM {vid} over {edge_name} '
          f'WHERE properties($$).{property_name} == "{property_value}"'
          f' YIELD properties($$).{property_name} as {property_name}, dst(edge) as vid')
    assert result.is_succeeded(), result.error_msg()
    print(result.column_values('vid'))
    if result.column_values('vid'):
        result = result.column_values('vid')[0].as_string()
    if start_session:
        session.release()
    return result


def find_destination(session, vid, edge_name, start_session=False, full_list=False):
    if start_session:
        session = chose_of_space()
    result = session.execute(f'GO FROM {vid} over {edge_name} YIELD dst(edge) as vid')
    print(f'GO FROM {vid} over {edge_name} YIELD dst(edge) as vid')
    assert result.is_succeeded(), result.error_msg()
    if start_session:
        session.release()
    if full_list:
        print('this')
        return result.column_values('vid')
    if result.column_values('vid'):
        print('that')
        result = result.column_values('vid')[0].as_string()
        return result
    return None


def fetch_vertex(session, vid, vertex_name, properties, start_session=False):
    if start_session:
        session = chose_of_space()
    result = session.execute(f'FETCH PROP ON {vertex_name} {vid} YIELD properties(vertex).{properties} as {properties}')
    print(f'FETCH PROP ON {vertex_name} {vid} YIELD properties(vertex).{properties} as {properties}')
    assert result.is_succeeded(), result.error_msg()
    if start_session:
        session.release()
    if properties in result.keys():
        if not result.column_values(properties)[0].is_null():
            return result.column_values(properties)[0].as_string()
    return None


def fetch_edge(session, source_vid, destination_vid, edge_name, properties, start_session=False):
    if start_session:
        session = chose_of_space()
    result = session.execute(f'FETCH PROP ON {edge_name} {source_vid} -> {destination_vid} '
                             f'YIELD properties(edge).{properties} as {properties};')
    print(f'FETCH PROP ON {edge_name} {source_vid} -> {destination_vid} '
          f'YIELD properties(edge).{properties} as {properties};')
    assert result.is_succeeded(), result.error_msg()
    if start_session:
        session.release()
    if result.column_values(properties)[0]:
        return result.column_values(properties)[0].as_string()
    return None


def yaml_deploy(cluster_vertex: data_classes.ClusterName, method_put=False):
    """ программа за четыре прохода создает шаблон в бд,
    за первый проход она размещается все узлы в бд, за второй создаёт соотвествующие связи
    """
    session = chose_of_space()
    if method_put:
        if is_unique_vid(session, cluster_vertex.vertex_type_system, cluster_vertex.vid):
            return '400 Cluster VID is not existed'
        else:
            delete_all_edge(session, cluster_vertex.vid, 'definition')
            delete_all_edge(session, cluster_vertex.vid, 'assignment')
            update_vertex(session, cluster_vertex.vertex_type_system, 'pure_yaml',
                          '"' + str(cluster_vertex.pure_yaml) + '"', cluster_vertex.vid)
    elif not (is_unique_vid(session, cluster_vertex.vertex_type_system, cluster_vertex.vid)):
        return '400 Cluster VID is not unique'
    print(type(cluster_vertex.pure_yaml))
    assignment_vertex: data_classes.AssignmentVertex
    for relationship_template in cluster_vertex.relationship_templates:
        relationship_template.set_vid(session)
        add_in_vertex(session, relationship_template.vertex_type_system, 'name', f'"{relationship_template.name}"',
                      relationship_template.vid)
    # добавление всех вершин связанных с definition vertex
    for assignment_vertex in cluster_vertex.assignment_vertex:
        assignment_vertex.set_vid(session)
        add_in_vertex(session, assignment_vertex.vertex_type_system,
                      'name, type', f'"{assignment_vertex.name}", "{assignment_vertex.vertex_type_tosca}"',
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
        for requirement_vertex in assignment_vertex.requirements:
            requirement_vertex: data_classes.Requirements
            requirement_vertex.set_vid(session)
            add_in_vertex(session, requirement_vertex.vertex_type_system, 'name', f'"{requirement_vertex.name}"',
                          requirement_vertex.vid)
            add_edge(session, 'requirements_destination', '', requirement_vertex.vid,
                     requirement_vertex.destination.vid, '')
            add_edge(session, 'requirements', '', assignment_vertex.vid, requirement_vertex.vid, '')
            add_edge(session, 'requirements', '', requirement_vertex.vid, requirement_vertex.relationship.vid, '')
            for capabilities_vertex in requirement_vertex.capabilities:
                add_edge(session, 'requirements_capability', '', requirement_vertex.vid, capabilities_vertex.vid, f'')

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
    interface_vertex: data_classes.DefinitionInterface
    # добавление всех interface_vertex
    for interface_vertex in cluster_vertex.interfaces_vertex:
        interface_vertex.set_vid(session)
        add_in_vertex(session, interface_vertex.vertex_type_system, 'vertex_type_tosca',
                      f'"{interface_vertex.vertex_type_tosca}"', interface_vertex.vid)
    # добавление всех relationship_vertex
    relationship_vertex: data_classes.RelationshipType
    for relationship_vertex in cluster_vertex.relationship_type:
        relationship_vertex.set_vid(session)
        add_in_vertex(session, relationship_vertex.vertex_type_system, 'vertex_type_tosca',
                      f'"{relationship_vertex.vertex_type_tosca}"', relationship_vertex.vid)
        for property_vertex in relationship_vertex.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'definition_property', 'name', relationship_vertex.vid, property_vertex.vid,
                     f'"{property_vertex.name}"')
    # добавление всех relationship_templates
    relationship_template: data_classes.RelationshipTemplate
    for relationship_template in cluster_vertex.relationship_templates:
        for property_vertex in relationship_template.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'definition_property', 'name', relationship_template.vid, property_vertex.vid,
                     f'"{property_vertex.name}"')
    # добавление всех definition_vertex
    definition_vertex: data_classes.DefinitionVertex
    for definition_vertex in cluster_vertex.definition_vertex:
        definition_vertex.set_vid(session)
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
        for capability_vertex, data in definition_vertex.capabilities.items():
            add_edge(session, 'definition_capability', 'name', definition_vertex.vid, capability_vertex.vid,
                     f'"{data}"')
        for interface_vertex, type_link in definition_vertex.interfaces.items():
            add_edge(session, 'definition_interface', 'name', definition_vertex.vid, interface_vertex.vid,
                     f'"{type_link}"')
    # добавление связей requirement в definition vertex

    # добавление связей derived_from

    for definition_vertex in cluster_vertex.definition_vertex:
        for derived in definition_vertex.derived_from:
            add_edge(session, 'derived_from', '', derived.vid, definition_vertex.vid,'')
        for requirement_vertex in definition_vertex.requirements:
            requirement_vertex: data_classes.Requirements
            requirement_vertex.set_vid(session)
            if requirement_vertex.occurrences != '':
                add_in_vertex(session, requirement_vertex.vertex_type_system, 'name ,occurrences',
                              f'"{requirement_vertex.name}","{str(requirement_vertex.occurrences)}"',
                              requirement_vertex.vid)
            else:
                add_in_vertex(session, requirement_vertex.vertex_type_system, 'name',
                              f'"{requirement_vertex.name}"', requirement_vertex.vid)
            add_edge(session, 'requirements_destination', '', requirement_vertex.vid,
                     requirement_vertex.destination.vid, '')
            add_edge(session, 'requirements', '', definition_vertex.vid, requirement_vertex.vid, '')
            add_edge(session, 'requirements', '', requirement_vertex.vid, requirement_vertex.relationship.vid, '')
            for capabilities_vertex in requirement_vertex.capabilities:
                add_edge(session, 'requirements_capability', '', requirement_vertex.vid, capabilities_vertex.vid, f'')

    for capability_vertex in cluster_vertex.definition_capabilities:
        capability_vertex: data_classes.DefinitionCapabilities
        for derived in capability_vertex.derived_from:
            add_edge(session, 'derived_from', '', capability_vertex.vid, derived.vid, '')
    for interface_vertex in cluster_vertex.interfaces_vertex:
        for derived in interface_vertex.derived_from:
            add_edge(session, 'derived_from', '', interface_vertex.vid, derived.vid, '')
        for property_vertex in interface_vertex.properties:
            property_vertex.set_vid(session)
            add_in_vertex(session, property_vertex.vertex_type_system, 'value_name, value',
                          f'"{property_vertex.value_name}", "{property_vertex.value}"', property_vertex.vid)
            add_edge(session, 'definition_property', 'name', interface_vertex.vid, property_vertex.vid,
                     f'"{property_vertex.name}"')
    for relationship_vertex in cluster_vertex.relationship_type:
        for derived in relationship_vertex.derived_from:
            add_edge(session, 'derived_from', '', relationship_vertex.vid, derived.vid, '')
        for target in relationship_vertex.valid_target_types:
            add_edge(session, 'valid_target_types', '', relationship_vertex.vid, target.vid, '')
    for relationship_template in cluster_vertex.relationship_templates:
        for type_relationship in relationship_template.type_relationship:
            add_edge(session, 'type_relationship', '', relationship_template.vid, type_relationship.vid, '')

    # доавление связей между cluster_vertex и всеми вершинами
    if not method_put:
        add_in_vertex(session, cluster_vertex.vertex_type_system, 'pure_yaml',
                      '"' + str(cluster_vertex.pure_yaml) + '"', cluster_vertex.vid)
    for assignment_vertex in cluster_vertex.assignment_vertex:
        add_edge(session, 'assignment', '', cluster_vertex.vid, assignment_vertex.vid, '')
    for definition_vertex in cluster_vertex.definition_vertex:
        add_edge(session, 'definition', '', cluster_vertex.vid, definition_vertex.vid, '')
    for relationship_vertex in cluster_vertex.relationship_type:
        add_edge(session, 'definition', '', cluster_vertex.vid, relationship_vertex.vid, '')
    for capability_vertex in cluster_vertex.definition_capabilities:
        add_edge(session, 'definition', '', cluster_vertex.vid, capability_vertex.vid, '')
    for relationship_template in cluster_vertex.relationship_templates:
        add_edge(session, 'assignment', '', cluster_vertex.vid, relationship_template.vid, '')
    # session.release()
    return '200 OK'
