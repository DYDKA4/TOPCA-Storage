import dpath.util

"""
yaml parser
return 
list of :
            [name_node, type_node, [list_of_depends],[list_of_properties_assignments],[list_of_capabilities]]
            [name_node, type_node, [list_of_depends],[list_of_properties_definition],[list_of_capabilities]]

list_of_depends can be [[]] :
            [[type_of_link, connects_to_name_node], ...]
list_of_properties_assignments can be [[]]:
            [[name, params], ...] 
list_of_properties_definition can be [[]]:
            [[name, params_type, params_default_value], ...] 
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


def parser(data):  # возвращает массив где каждый элдемент сожержимт в себе информаию: имя, тип узла, завимости.
    # print(json.dumps(data, indent=2))
    node_templates = find_node_templates(data)
    # print(node_templates)
    data_assignments = []
    data_definition = []
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
    if data.get('node_types'):
        for name_of_node, params in data.get('node_types').items():
            ans = [name_of_node.replace('.', '_')]
            print(name_of_node)
            if params.get('properties'):
                for properties, values in params.get('properties').items():
                    tmp = []
                    # print(properties, values)
                    for values_def, values_props in values.items():
                        tmp += [[properties+"_"+values_def, str(values_props).replace('\n', ' ')]]
                ans += [tmp]
            else:
                ans += [[[]]]
            data_definition += [ans]
    return data_assignments, data_definition
