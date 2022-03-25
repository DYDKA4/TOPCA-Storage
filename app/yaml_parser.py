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


def find_property(val, vertex):
    if val.get('properties'):
        for name_value, value in val.get('properties').items():
            print(name_value, value)
            for properties_name, properties_value in value.items():
                vertex_properties = data_classes.DefinitionProperties(name_value, properties_name,
                                                                      str(properties_value).replace('\n', ' '))
                vertex.add_properties(vertex_properties)


def form_list_of_vertex(yaml, list_of_vertex: list, type_of_vertex: str, class_of_object, find_property_flag=False,
                        interface_flag=False):
    for type_node, val in yaml.get(type_of_vertex).items():
        vertex = class_of_object(type_node)
        if find_property_flag:
            find_property(val, vertex)
        if interface_flag:
            for key, value in val.items():
                if key != 'derived_from' and key != 'description':
                    vertex_properties = data_classes.DefinitionProperties(key, 'Function',
                                                                          str(value).replace('\n', ' '))
                    vertex.add_properties(vertex_properties)
        list_of_vertex.append(vertex)


def linking_derived_from(val, type_of_vertex, name):
    source = find_vertex(val.get('derived_from'), type_of_vertex, search_by_type=True)
    destination = find_vertex(name, type_of_vertex, search_by_type=True)
    source.add_derived_from(destination)


def parser(data, cluster_name):
    node_templates = find_node_templates(data)
    # формирование списка relationship_templates
    relationship_templates = []
    templates_data = dpath.util.get(data, "topology_template/relationship_templates")
    for relationship_template, val in templates_data.items():
        vertex = data_classes.RelationshipTemplate(relationship_template)
        if val.get('properties'):
            for name_value, value in val.get('properties').items():
                vertex_properties = data_classes.DefinitionProperties(name_value, name_value,
                                                                      str(value).replace('\n', ' '))
                vertex.add_properties(vertex_properties)
        relationship_templates.append(vertex)
    # новая классовая система
    assignments_vertex = []
    for name, value in node_templates.items():
        vertex_type = value.get('type')
        vertex = data_classes.AssignmentVertex(name, vertex_type)
        if value.get('capabilities'):
            for capabilities_name, capabilities in value.get('capabilities').items():
                vertex_capabilities = data_classes.AssignmentCapabilities(capabilities_name)
                if capabilities.get('properties'):
                    for properties_name, properties_value in capabilities.get('properties').items():
                        vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                        vertex_capabilities.add_properties(vertex_properties)
                vertex.add_capabilities(vertex_capabilities)
        if value.get('properties'):
            for properties_name, properties_value in value.get('properties').items():
                vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                vertex.add_properties(vertex_properties)
        assignments_vertex.append(vertex)

    # добавление requirements
    for name, value in node_templates.items():
        if value.get('requirements'):
            if type(value.get('requirements')) is list:
                for requirement in value.get('requirements'):
                    for requirement_name, link in requirement.items():
                        print(requirement_name, link)
                        source = find_vertex(name, assignments_vertex)
                        if link.get('node'):
                            dest = find_vertex(link['node'], assignments_vertex)

                            requirement_vertex = data_classes.Requirements(requirement_name, source,
                                                                           destination=dest)
                        else:
                            requirement_vertex = data_classes.Requirements(requirement_name, source)
                        if link.get('node_filter'):
                            node_filter_data = link.get('node_filter')
                            node_filter = data_classes.NodeFilter()
                            if node_filter_data.get('properties'):
                                for properties in node_filter_data.get('properties'):
                                    for properties_name, properties_value in properties.items():
                                        vertex_properties = data_classes.AssignmentProperties(properties_name,
                                                                                              properties_value)
                                        node_filter.add_properties(vertex_properties)
                                    requirement_vertex.set_node_filter(node_filter)
                        if link.get('relationship'):
                            relationship = find_vertex(link['relationship'], relationship_templates)
                            requirement_vertex.set_relationship(relationship)
                            source.add_requirements(requirement_vertex)
            if type(value.get('requirements')) is dict:
                print('REQUIREMENTS id DICT')

    # формирование списка definition_vertex c properties
    definition_vertex = []
    form_list_of_vertex(data, definition_vertex, 'node_types',
                        data_classes.DefinitionVertex, find_property_flag=True)
    # формирование списка capabilities
    capabilities_vertex = []
    form_list_of_vertex(data, capabilities_vertex, 'capability_types',
                        data_classes.DefinitionCapabilities, find_property_flag=True)
    # формирование спика interface
    interfaces_vertex = []
    form_list_of_vertex(data, interfaces_vertex, 'interface_types',
                        data_classes.DefinitionInterface, interface_flag=True)
    # формирование списка relationship_vertex
    relationship_vertex = []
    form_list_of_vertex(data, relationship_vertex, 'relationship_types',
                        data_classes.RelationshipType, find_property_flag=True)

    # формирование связей между definition_vertex и другими
    for name, val in data.get('node_types').items():
        if val.get('capabilities'):
            for key, capabilities in val.get('capabilities').items():
                source: data_classes.DefinitionVertex
                destination = find_vertex(capabilities.get('type'), capabilities_vertex, search_by_type=True)
                source = find_vertex(name, definition_vertex, search_by_type=True)
                source.add_capabilities(destination, key)
        if val.get('derived_from'):
            linking_derived_from(val, definition_vertex, name)
        if val.get('interfaces'):
            for link_type, interface in val.get('interfaces').items():
                destination = find_vertex(interface.get('type'), interfaces_vertex, search_by_type=True)
                source = find_vertex(name, definition_vertex, search_by_type=True)
                source.add_interface(destination, link_type)
        if val.get('requirements'):
            if type(val.get('requirements')) is list:
                for requirement in val.get('requirements'):
                    for requirement_name, link in requirement.items():
                        source = find_vertex(name, definition_vertex, search_by_type=True)
                        if link.get('node'):
                            dest = find_vertex(link['node'], definition_vertex, search_by_type=True)
                            requirement_vertex = data_classes.Requirements(requirement_name, source,
                                                                           destination=dest)
                        else:
                            requirement_vertex = data_classes.Requirements(requirement_name, source)
                        print(link)
                        if link.get('node_filter'):
                            node_filter_data = link.get('node_filter')
                            node_filter = data_classes.NodeFilter()
                            if node_filter_data.get('properties'):
                                for properties in node_filter_data.get('properties'):
                                    for properties_name, properties_value in properties.items():
                                        vertex_properties = data_classes.AssignmentProperties(properties_name,
                                                                                              properties_value)
                                        node_filter.add_properties(vertex_properties)
                                    requirement_vertex.set_node_filter(node_filter)

                        if link.get('relationship'):
                            relationship = find_vertex(link['relationship'], relationship_vertex, search_by_type=True)
                            requirement_vertex.set_relationship(relationship)
                        if link.get('capability'):
                            destination = find_vertex(link.get('capability'), capabilities_vertex,
                                                      search_by_type=True)
                            requirement_vertex.add_capabilities(destination)
                        if link.get('occurrences'):
                            requirement_vertex.set_occurrences(link.get('occurrences'))
                        source.add_requirements(requirement_vertex)
            if type(val.get('requirements')) is dict:
                print('REQUIREMENTS id DICT')
    # формирование связей между capability
    for name, val in data.get('capability_types').items():
        if val.get('derived_from'):
            linking_derived_from(val, capabilities_vertex, name)
    # формирование связей между interface
    for name, val in data.get('interface_types').items():
        if val.get('derived_from'):
            linking_derived_from(val, interfaces_vertex, name)

    # формирование связей между relationship
    for name, val in data.get('relationship_types').items():
        source: data_classes.RelationshipType
        if val.get('derived_from'):
            linking_derived_from(val, relationship_vertex, name)
        if val.get('valid_target_types'):
            for capabilities_type in val.get('valid_target_types'):
                source = find_vertex(name, relationship_vertex, search_by_type=True)
                destination = find_vertex(capabilities_type, capabilities_vertex, search_by_type=True)
                source.add_valid_target_types(destination)
    # формирование связей между relationship_templates
    for name, val in templates_data.items():
        src: data_classes.RelationshipTemplate
        if val.get('type'):
            src = find_vertex(name, relationship_templates)
            destination = find_vertex(val.get('type'), relationship_vertex, search_by_type=True)
            src.add_type_relationship(destination)
    outputs = []
    output_data = data.get('topology_template')
    for name, val in output_data.get('outputs').items():
        output = data_classes.Outputs(name)
        if val.get('value'):
            output.set_value(val.get('value'))
        if val.get('description'):
            output.set_description(val.get('description'))
        outputs.append(output)
    # P.S скорее всего можно либо сделать методы в data_classes либо придумать функции для уменьшения частичного повторения кода
    vertex_cluster = data_classes.ClusterName(cluster_name, data, definition_vertex,
                                              assignments_vertex, capabilities_vertex,
                                              interfaces_vertex, relationship_vertex,
                                              relationship_templates, outputs)
    for i in vertex_cluster.definition_vertex:
        for j in i.capabilities.values():
            print(j)
    print(outputs)
    return vertex_cluster
