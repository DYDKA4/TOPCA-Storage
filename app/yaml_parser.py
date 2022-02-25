import dpath.util
from app import data_classes

"""
yaml parser
return 
list of :
            [name_node, type_node, [list_of_depends],[list_of_properties_assignments],[list_of_capabilities]]
            [type_node, [list_of_properties_definition][capability_types, ...]]
            [capability_types, [list_of_properties_definition]]

list_of_depends can be [[]] :
            [[type_of_link, connects_to_name_node], ...]
list_of_properties_assignments can be [[]]:
            [[name, params], ...] 
list_of_properties_definition can be [[]]:
            [[name, params_type, params_default_value], ...] 
list_of_capabilities_definition can be [[]]:
            [[]]
list_of_capabilities can be [[]] :
            [name_of_capabilities, name_of_capabilities, [list_of_properties_assignments]]
"""


# первое что надо найти где расположена часть с ключём node_templates
def find_node_templates(data):
    node_template = dpath.util.get(data, "topology_template/node_templates")
    return node_template


def separation(data):
    return data.split('.', -1)[-1]


def local_storage_parser(data):
    # print(data)
    data = data.get('local_storage')
    node = data.get('node')
    relationship = data.get('relationship')
    if type(relationship) == dict:
        return [[relationship.get('type'), node]]
    else:
        return [[relationship, node]]


def requirements_parser(data):
    result = []
    if type(data) == dict:
        print('DICT')
        print(data.items())
    elif type(data) == list:
        for link in data:
            if 'local_storage' in link.keys():
                print("LOCAL STORAGE")
                return local_storage_parser(link)
            else:
                for key in link:
                    result += [[key, link.get(key)]]
        return result
    else:
        print('ELSE')
    return


def find_requirements(data):
    res = data.get('requirements')
    if res:
        # print(data.get('requirements'), '\n')
        return requirements_parser(res)
    return


def find_properties(data):
    res = data.get('properties')
    if res:
        result = []
        if type(res) == dict:
            for key, value in res.items():
                result += [[key, str(value)]]
        return result
    return


def find_capabilities(data):
    res = data.get('capabilities')
    if res:
        result = []
        if type(res) == dict:
            for key, value in res.items():
                result += [key, find_properties(value)]

        return result
    return


def forming_capabilities(data, name):
    answer = []
    if data.get(name):
        for name_of_node, params in data.get(name).items():
            ans = [name_of_node.replace('.', '_')]
            if params.get('properties'):
                for properties, values in params.get('properties').items():
                    tmp = []
                    # print(properties, values)
                    for values_def, values_props in values.items():
                        tmp += [[properties + "_" + values_def, str(values_props).replace('\n', ' ')]]
                    ans += [tmp]
            else:
                ans += [[[]]]
            answer += [ans]
        return answer


def find_name(capability_types, value, converting_literal, converting_literal_into):
    for index in range(len(capability_types)):
        if str(value).replace(converting_literal, converting_literal_into) in capability_types[index]:
            print(capability_types[index][0], hex(id(capability_types[index][0])), 'capability_typex id',
                  hex(id(capability_types)))
            return capability_types[index][0]
    return []


def parser(data):  # возвращает массив где каждый элдемент сожержимт в себе информаию: имя, тип узла, завимости.
    # print(json.dumps(data, indent=2))
    node_templates = find_node_templates(data)
    # print(node_templates)
    data_assignments = []
    node_types = []
    capability_types = []
    for name_of_node, params in node_templates.items():
        ans = []
        node_type = params.get('type')
        node_type = separation(node_type)  # упрощение типа ноды
        requirements = find_requirements(params)
        properties = find_properties(params)
        capabilities = find_capabilities(params)
        print(capabilities)
        ans += [name_of_node]
        ans += [node_type]
        if requirements:
            ans += [requirements]
        else:
            ans += [[[]]]
        if properties:
            ans += [properties]
        else:
            ans += [[[]]]
        if capabilities:
            ans += [capabilities]
        else:
            ans += [[[]]]
        data_assignments += [ans]
    # получение списка node_types
    # возможно пора переходить к классам
    # node_types = forming_capabilities(data, 'node_types')
    if data.get('node_types'):
        for name_of_node, params in data.get('node_types').items():
            ans = [name_of_node.replace('.', '_')]
            print(name_of_node)
            if params.get('properties'):
                for properties, values in params.get('properties').items():
                    tmp = []
                    # print(properties, values)
                    for values_def, values_props in values.items():
                        tmp += [[properties + "_" + values_def, str(values_props).replace('\n', ' ')]]
                ans += [tmp]
            else:
                ans += [[[]]]
            node_types += [ans]
    capability_types = forming_capabilities(data, 'capability_types')
    if node_types:
        i = 0  # выглядит как костыль
        for name_of_node, params in data.get('node_types').items():
            if params.get('capabilities'):
                tmp = []
                for type_capabilities, values in params.get('capabilities').items():
                    print(type_capabilities, values)
                    if values.get('type'):
                        # print('after function', hex(id(find_name(capability_types, values.get('type'), '.', '_'))))
                        # tmp += [find_name(capability_types,values.get('type'), '.', '_')]
                        for index in range(len(capability_types)):
                            if str(values.get('type')).replace('.', '_') in capability_types[index]:
                                tmp += [[type_capabilities, capability_types[index][0]]]
            else:
                tmp = [[]]
            node_types[i] += [tmp]
            i += 1

    node_templates = find_node_templates(data)
    l = []
    for name, value in node_templates.items():
        print(name, value)
        vertex_type = value.get('type')
        vertex = data_classes.AssignmentVertex(name, vertex_type)
        if value.get('capabilities'):
            for capabilities_name, capabilities in value.get('capabilities').items():
                vertex_capabilities = data_classes.AssignmentCapabilities(capabilities_name)
                print('PROPS', capabilities_name, capabilities)
                if capabilities.get('properties'):
                    for properties_name, properties_value in capabilities.get('properties').items():
                        print(properties_name, properties_value)
                        vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                        vertex_capabilities.add_properties(vertex_properties)
                vertex.add_capabilities(vertex_capabilities)
        if value.get('properties'):
            for properties_name, properties_value in value.get('properties').items():
                print(properties_name, properties_value)
                vertex_properties = data_classes.AssignmentProperties(properties_name, properties_value)
                vertex.add_properties(vertex_properties)
        l.append(vertex)
    print()
    for i in l:
        print(i)
    return data_assignments, node_types, capability_types
