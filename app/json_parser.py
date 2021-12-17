import json


def myprint(d):
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v)
        else:
            print("{0} : {1}".format(k, v))


def search_in_dict(d, key):
    for k, v in d.items():
        if k == key:
            return v
        if isinstance(v, dict):
            search_in_dict(v, key)
            return v


def host_parser(d):
    cpu = ram = mem = None
    d = d['properties']
    for key in d:
        if key == 'disk_size':
            mem = d[key]
        elif key == 'num_cpus':
            cpu = d[key]
        elif key == 'mem_size':
            ram = d[key]
    return cpu, ram, mem


def compute_parser(d):
    cpu = ram = mem = None
    # print(d)
    for key in d['capabilities']:
        if key == 'host':
            cpu, ram, mem = host_parser(d['capabilities'][key])
    print(d['requirements'])
    print(type(d['requirements']))
    for elem in d['requirements']:
        print(elem)

        # in future be able to parse and os properties
    # myprint(d)
    return [cpu, ram, mem]


def parser(data):
    cpu = ram = mem = None
    node_templates = search_in_dict(data, 'node_templates')['node_templates']  # скорее всего можно как-то последнию
    # операцию по ключу сделать в search_dict но пока хз как
    # print(node_templates)
    # print(node_templates.keys())
    # myprint(node_templates)
    Computes = []  # compute node characteristics
    Block_Storage_Counter = 0
    for key in node_templates:
        # parser of Compute_node
        if node_templates[key]['type'] == 'Compute':
            Computes += [compute_parser(node_templates[key])]
        if node_templates[key]['type'] == 'BlockStorage':
            #костыль
            #пока что нету адекватного решения
            Block_Storage_Counter += 1

    return
