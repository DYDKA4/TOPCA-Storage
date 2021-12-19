import dpath.util

list_of_relationship_type = [
    'DependsOn',
    'HostedOn',
    'ConnectsTo',
    'AttachesTo',
    'RoutesTo',
]


# первое что надо найти где расположена часть с ключём node_templates
def find_node_templates(data):
    node_template = dpath.util.get(data, "topology_template/node_templates")
    return node_template


def separation(data):
    stripped = data.split('.', -1)
    return data


def find_requirements(data, source):
    data = data.get('requirements')
    if data:
        data = data[0]  # пока не понятно когда список размера не 1
        depends = dpath.util.get(data, 'local_storage/node')
        type_of_depends = dpath.util.get(data, 'local_storage/relationship')
        if type(type_of_depends) == dict:
            type_of_depends = type_of_depends.get('type')
        else:  # поиск кастомного типа отношений и поиск в нем типа зависимости
            type_of_depends = dpath.util.get(source, f'topology_template/relationship_templates/{type_of_depends}/type')
        if type_of_depends not in list_of_relationship_type:  # определние кастомного отношнеия к 5 стандартным
            type_of_depends = dpath.util.get(source, f'relationship_types/{type_of_depends}/derived_from')
            if type_of_depends not in list_of_relationship_type:
                type_of_depends = type_of_depends.split('.', -1)[-1]

        return [depends, type_of_depends]
    return data


def parser(data):  # возвращает массив где каждый элдемент сожержимт в себе информаию: имя, тип узла, завимости.
    # print(json.dumps(data, indent=2))
    node_templates = find_node_templates(data)
    # print(node_templates)
    answer = []
    for name_of_node, params in node_templates.items():
        ans = []
        node_type = params.get('type')
        requirements = find_requirements(params, data)
        ans += [name_of_node]
        ans += [node_type]
        if requirements:
            ans += [requirements]
        answer += [ans]
    return answer
