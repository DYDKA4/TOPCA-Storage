from flask import request, abort
from app import app
from nebula_communication import communication_with_nebula
import yaml
from app import constructor_yaml
from app import find as find_method
from nebula_communication.deploy import deploy
from nebula_communication.redis_communication import add_vid, delete_all
from nebula_communication.update_template.update_template import update_template
from parser.linker.tosca_v_1_3.main_linker import main_linker
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import service_template_definition_parser


@app.route('/yaml-template/', methods=['POST', 'PUT', 'GET'])
# curl -X POST -F file=@jamlExamples/service_template.yaml  http://127.0.0.1:5000/yaml-template/?cluster_name=cluster
def yaml_add():
    cluster_name = request.args.get('cluster_name')
    if request.method in ['POST', 'PUT']:
        file = request.files['file']
        if file:
            file = file.read().decode("utf-8")
            file = yaml.safe_load(file)
        else:
            abort(400)
        if cluster_name:
            template = service_template_definition_parser(cluster_name, file)
            main_linker(template)
            if add_vid(template.name, template.name):
                abort(400)
            if request.method == 'POST':
                print('DEPLOY START')
                deploy(template, template.name)
            # else:
            #     end_code = communication_with_nebula.yaml_deploy(cluster_vertex, method_put=True)
            print()
            return f'{200}'
    if request.method == 'GET':
        """
        curl -X GET 'http://127.0.0.1:5000/yaml-template/?cluster_name=cluster_tosca_59'
        """
        yaml_collection = constructor_yaml.get_yaml(cluster_name)

        return f'{yaml_collection}'

    return '''
            400 Bad Request 
            '''


@app.route('/yaml-template/<path:varargs>', methods=['PATCH'])
def yaml_update(varargs=None):
    """
    curl -X PATCH
    Поддерживаемые пути:
    'http://127.0.0.1:5000/yaml-template/topology_template/relationship_templates/*template_name*/type?cluster_
    name=*new_value*'
    """
    varargs = varargs.split("/")
    cluster_name = varargs[0]
    varargs = varargs[1:]
    value = request.args.get('value')
    value_name = request.args.get('value_name')
    type_update = request.args.get('type_update')
    if type_update is None:
        type_update = ""
    elif type_update not in {'delete', 'add'}:
        abort(400)
    print(value_name, value, cluster_name, varargs)
    if not value_name or not value:
        abort(400)
    update_template(cluster_name, value, value_name, varargs, type_update)
    return f'{value_name} = {value} in cluster: {cluster_name}'


@app.route('/yaml-delete', methods=['PATCH'])
# curl -X PATCH http://127.0.0.1:5000/yaml-delete
def yaml_patch():
    delete_all()
    return "200 OK"


@app.route('/find/<path:varargs>', methods=['GET'])
def find(varargs=None):
    search_by = request.args.get('search_by')
    cluster_name = request.args.get('cluster_name')
    find_cluster_name = request.args.get('find_cluster_name')
    node_vid = request.args.get('node_vid')
    requirement_name = request.args.get('requirement_name')
    return find_method.find_node(varargs, search_by, cluster_name, find_cluster_name, requirement_name)


@app.route('/download_yaml', methods=['GET'])
def get_yaml_from_vertex():
    """
     curl -X GET 'http://127.0.0.1:5000/download_yaml?vid=AssignmentVertex3'
    :return:
    """
    vid = request.args.get('vid')
    result = constructor_yaml.separated_vertex(vid)
    return f'{result}'
