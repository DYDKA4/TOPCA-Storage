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
                    vertex_properties = data_classes.DefinitionProperties(name_value, properties_name,
                                                                          str(properties_value).replace('\n', ' '))
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
                    vertex_properties = data_classes.DefinitionProperties(name_value, properties_name,
                                                                          str(properties_value).replace('\n', ' '))
                    vertex.add_properties(vertex_properties)
        capabilities_vertex.append(vertex)
    # формирование спика interface
    interfaces_vertex = []
    for interface_type, val in data.get('interface_types').items():
        vertex = data_classes.DefinitionInterface(interface_type)
        interfaces_vertex.append(vertex)
    # формирование списка relationship_vertex
    relationship_vertex = []
    for relationship_type, val in data.get('relationship_types').items():
        vertex = data_classes.RelationshipType(relationship_type)

        if val.get('properties'):
            for name_value, value in val.get('properties').items():
                # print(name_value, value)
                for properties_name, properties_value in value.items():
                    vertex_properties = data_classes.DefinitionProperties(name_value, properties_name,
                                                                          str(properties_value).replace('\n', ' '))
                    vertex.add_properties(vertex_properties)
        relationship_vertex.append(vertex)
    # формирование списка relationship_templates
    relationship_templates = []
    templates_data = dpath.util.get(data, "topology_template/relationship_templates")
    print(templates_data)
    for relationship_template, val in templates_data.items():
        vertex = data_classes.RelationshipTemplate(relationship_template)
        print(relationship_template, val)
        if val.get('properties'):
            for name_value, value in val.get('properties').items():
                print(name_value, value)
                vertex_properties = data_classes.DefinitionProperties(name_value, name_value,
                                                                          str(value).replace('\n', ' '))
                vertex.add_properties(vertex_properties)
        relationship_templates.append(vertex)
    # формирование связей между definition_vertex и другими
    for name, val in data.get('node_types').items():
        if val.get('capabilities'):
            for capabilities in val.get('capabilities').values():
                destination = find_vertex(capabilities.get('type'), capabilities_vertex, search_by_type=True)
                source = find_vertex(name, definition_vertex, search_by_type=True)
                source.add_capabilities(destination)
        if val.get('derived_from'):
            source = find_vertex(val.get('derived_from'), definition_vertex, search_by_type=True)
            destination = find_vertex(name, definition_vertex, search_by_type=True)
            source.add_derived_from(destination)
        if val.get('interfaces'):
            for link_type, interface in val.get('interfaces').items():
                destination = find_vertex(interface.get('type'), interfaces_vertex,search_by_type=True)
                source = find_vertex(name, definition_vertex, search_by_type=True)
                source.add_interface(destination, link_type)
        if val.get('requirements'):
            if type(val.get('requirements')) is list:
                for requirement in val.get('requirements'):
                    # print(requirement)
                    for link in requirement.values():
                        dest = find_vertex(link['node'], definition_vertex, search_by_type=True)
                        source = find_vertex(name, definition_vertex, search_by_type=True)
                        source.add_requirements(dest, link['relationship'])
            if type(val.get('requirements')) is dict:
                print('REQUIREMENTS id DICT')
    # формирование связей между capability
    for name, val in data.get('capability_types').items():
        if val.get('derived_from'):
            source = find_vertex(val.get('derived_from'), capabilities_vertex, search_by_type=True)
            destination = find_vertex(name, capabilities_vertex, search_by_type=True)
            source.add_derived_from(destination)
    # формирование связей между interface
    for name, val in data.get('interface_types').items():
        if val.get('derived_from'):
            source = find_vertex(val.get('derived_from'), interfaces_vertex, search_by_type=True)
            destination = find_vertex(name, interfaces_vertex, search_by_type=True)
            source.add_derived_from(destination)

    # формирование связей между relationship
    for name, val in data.get('relationship_types').items():
        source: data_classes.RelationshipType
        if val.get('derived_from'):
            source = find_vertex(val.get('derived_from'), relationship_vertex, search_by_type=True)
            destination = find_vertex(name, relationship_vertex, search_by_type=True)
            source.add_derived_from(destination)
        if val.get('valid_target_types'):
            for capabilities_type in val.get('valid_target_types'):
                source = find_vertex(name, relationship_vertex, search_by_type=True)
                destination = find_vertex(capabilities_type, capabilities_vertex, search_by_type=True)
                source.add_valid_target_types(destination)
    # формирование связей между relationship_templates
    for name, val in templates_data.items():
        src: data_classes.RelationshipTemplate
        if val.get('type'):
            print(name)
            src = find_vertex(name, relationship_templates)
            print(src)
            destination = find_vertex(val.get('type'), relationship_vertex, search_by_type=True)
            print('DESTINATION', destination)
            src.add_type_relationship(destination)
    # P.S скорее всего можно либо сделать методы в data_classes либо придумать функции для уменьшения частичного повторения кода
    for i in definition_vertex:
        print(i)

    print()
    for i in capabilities_vertex:
        print(i)
    print()
    for i in interfaces_vertex:
        print(i)
    print()
    for i in relationship_vertex:
        print(i)
    print()
    for i in assignments_vertex:
        print(i)
    print()
    vertex_cluster = data_classes.ClusterName(cluster_name, data, definition_vertex,
                                              assignments_vertex, capabilities_vertex,
                                              interfaces_vertex, relationship_vertex,
                                              relationship_templates)
    print(vertex_cluster)
    return vertex_cluster
