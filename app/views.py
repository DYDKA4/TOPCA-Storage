from flask import request
from app import app
from app import communication_with_nebula
from app import yaml_parser
import yaml
import dpath.util


@app.route('/yaml-template/', methods=['POST', 'PUT'])
@app.route('/yaml-template/<path:varargs>', methods=['PATCH'])
# curl -F file=@jamlExamples/SBS.yaml http://127.0.0.1:5000/yaml-template?cluster_name="cluster"
def yaml_add(varargs=None):
    cluster_name = request.args.get('cluster_name')
    if request.method != 'PATCH':
        file = request.files['file']
        if file:
            file = file.read().decode("utf-8")
            file = yaml.safe_load(file)
            pure_yaml = file
        else:
            return '''
            400 Bad Request 
            '''
        print(pure_yaml)
        if cluster_name:
            cluster_vertex = yaml_parser.parser(file, cluster_name)
            cluster_vertex.pure_yaml = pure_yaml
            end_code = '400'
            if request.method == 'POST':
                end_code = communication_with_nebula.yaml_deploy(cluster_vertex)
            else:
                end_code = communication_with_nebula.yaml_deploy(cluster_vertex, method_put=True)
            print()
            return f'{end_code}'
    if request.method == 'PATCH':
        '''
        curl -X PATCH 'http://127.0.0.1:5000/yaml-template/topology_template/relationship_templates?cluster_name=10&name=ab'
        Поддерживаемые пути: 
        topology_template/relationship_templates/?name=*new_name*
        '''
        print(varargs)
        copy_varargs = varargs
        varargs = varargs.split("/")
        new_value = request.args.get('new_value')
        pure_yaml = communication_with_nebula.get_yaml_from_cluster(cluster_name)
        pure_yaml = yaml.safe_load(pure_yaml)
        data = pure_yaml
        # поиск нужного ключа в yaml шаблоне и замена его
        for key in varargs:
            if data.get(key):
                data = data[key]

                print(data)
            else:
                return '400 Bad Path'
        pure_yaml = pure_yaml.dpath.util.set(pure_yaml, varargs, new_value,)
        print(pure_yaml)
        data = new_value
        print(pure_yaml)
        return f'{varargs} {cluster_name} {new_value}\n{data}'
    return '''
            400 Bad Request 
            '''


@app.route('/yaml-patch', methods=['PATCH'])
# curl -X PATCH -F file=@jamlExamples/SBS.yaml http://127.0.0.1:5000/yaml-patch?cluster_name=cluster_tosca_46
def yaml_patch():
    """

    :return:
    """
    cluster_name = request.args.get('cluster_name')
    if cluster_name:
        end_code = '400'
        return f'{end_code}'
    return '''
            400 Bad Request 
            '''


@app.route('/node_templates/<string:node_name>/capabilities/<string:name_of_capability>')
def allow(node_name, name_of_capability):
    return f'{node_name}, {name_of_capability}'


@app.route('/topology_template/node_templates/<string:node_name>/capabilities/<string:name_of_capability>')
def asd(node_name, name_of_capability):
    return f'{node_name}, {name_of_capability}'