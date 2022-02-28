import dpath.util
from app import data_classes


# первое что надо найти где расположена часть с ключём node_templates
def find_node_templates(data):
    node_template = dpath.util.get(data, "topology_template/node_templates")
    return node_template


def find_vertex(name, list_of_vertex, search_by_type=False):
    for vertex in list_of_vertex:
        if search_by_type:
            if vertex.vertex_type_tosca == name:
                return vertex

        else:
            if vertex.name == name:
                return vertex
    return


def parser(data, cluster_name):  # возвращает массив где каждый элдемент сожержимт в себе информаию: имя, тип узла, завимости.
    # print(json.dumps(data, indent=2))
    node_templates = find_node_templates(data)
    # новая классовая система
    assignments_vertex = []
    for name, value in node_templates.items():
        # print(name, value)
        vertex_type = value.get('type')
        vertex = data_classes.AssignmentVertex(name, vertex_type)
        if value.get('capabilities'):
            for capabilities_name, capabilities in value.get('capabilities').items():
                vertex_capabilities = data_classes.AssignmentCapabilities(capabilities_name)
                # print('PROPS', capabilities_name, capabilities)
                if capabilities.get('properties'):
                    for properties_name, properties_value in capabilities.get('properties').items():
                        # print(properties_name, properties_value)
                        vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                        vertex_capabilities.add_properties(vertex_properties)
                vertex.add_capabilities(vertex_capabilities)
        if value.get('properties'):
            for properties_name, properties_value in value.get('properties').items():
                # print(properties_name, properties_value)
                vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                vertex.add_properties(vertex_properties)
        assignments_vertex.append(vertex)

    # добавление requirements
    for name, value in node_templates.items():
        if value.get('requirements'):
            if type(value.get('requirements')) is list:
                for requirement in value.get('requirements'):
                    # print(requirement)
                    for link in requirement.values():
                        dest = find_vertex(link['node'], assignments_vertex)
                        source = find_vertex(name, assignments_vertex)
                        source.add_requirements(dest, link['relationship'])
            if type(value.get('requirements')) is dict:
                print('REQUIREMENTS id DICT')

    # формирование списка definition_vertex c properties
    definition_vertex = []
    for type_node, val in data.get('node_types').items():
        # print(type_node)
        vertex = data_classes.DefinitionVertex(type_node)
        if val.get('properties'):
            for name_value, value in val.get('properties').items():
                # print(name_value, value)
                for properties_name, properties_value in value.items():
                    vertex_properties = data_classes.DefinitionProperties(name_value, properties_name, properties_value)
                    vertex.add_properties(vertex_properties)
        definition_vertex.append(vertex)

    # формирование списка capabilities
    capabilities_vertex = []
    for capability_type, val in data.get('capability_types').items():
        # print(capability_type)
        vertex = data_classes.DefinitionCapabilities(capability_type)
        if val.get('properties'):
            for name_value, value in val.get('properties').items():
                # print(name_value, value)
                for properties_name, properties_value in value.items():
                    vertex_properties = data_classes.DefinitionProperties(name_value, properties_name, properties_value)
                    vertex.add_properties(vertex_properties)
        capabilities_vertex.append(vertex)

    # формирование связей между capabilities и definition_vertex

    for name, val in data.get('node_types').items():
        if val.get('capabilities'):
            for capabilities in val.get('capabilities').values():
                destination = find_vertex(capabilities.get('type'), capabilities_vertex, search_by_type=True)
                source = find_vertex(name, definition_vertex, search_by_type=True)
                source.add_capabilities(destination)


    # P.S скорее всего можно либо сделать методы в data_classes либо придумать функции для уменьшения частичного повторения кода

    # for i in definition_vertex:
    #     print(i)

    # print()
    #
    for i in assignments_vertex:
        print(i)

    vertex_cluster = data_classes.ClusterName(cluster_name, data, definition_vertex, assignments_vertex)
    print(vertex_cluster)
    return vertex_cluster
