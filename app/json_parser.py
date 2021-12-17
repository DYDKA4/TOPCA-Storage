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
            print(d[key])
            mem = d[key]
        elif key == 'num_cpus':
            cpu = d[key]
        elif key == 'mem_size':
            ram = d[key]
    return cpu, ram, mem


def compute_parser(d):
    cpu = ram = mem = None
    print(d.keys())
    for key in d:
        if key == 'host':
            cpu, ram, mem = host_parser(d[key])
        print(d[key])
    print(cpu, ram, mem)
    # myprint(d)
    return cpu, ram, mem


def parser(data):
    cpu = ram = mem = None
    node_templates = search_in_dict(data, 'node_templates')['node_templates']  # скорее всего можно как-то последнию
    # операцию по ключу сделать в search_dict но пока хз как
    # print(node_templates)
    # print(node_templates.keys())
    for key in node_templates:
        if node_templates[key]['type'] == 'Compute':
            cpu, ram, mem = compute_parser(node_templates[key]['capabilities'])

    return cpu, ram, mem
