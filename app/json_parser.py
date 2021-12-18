import json
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
    node_template = dict
    node_template = dpath.util.get(data, "topology_template/node_templates")
    return node_template


def search_custom(data,source):
    print("SEARCH")
    return


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
        if type_of_depends not in list_of_relationship_type:
            type_of_depends = dpath.util.get(source, f'relationship_types/{type_of_depends}/derived_from')
        return [depends, type_of_depends]
    return data


def parser(data):
    cpu = ram = mem = None
    # print(json.dumps(data, indent=2))
    node_templates = find_node_templates(data)
    # print(node_templates)
    for name_of_node, params in node_templates.items():
        node_type = params.get('type')
        requirements = find_requirements(params,data)

        print(requirements)
        print(node_type)
    return
