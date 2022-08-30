import logging

from flask import request, abort, render_template, Response, jsonify, make_response
from werkzeug.exceptions import HTTPException

from app import app, current_api_version as cav
import yaml
from nebula_communication.deploy import deploy
from nebula_communication.nebula_functions import delete_all, delete_cluster, find_vertex_by_properties, fetch_vertex
from nebula_communication.redis_communication import add_vid
from nebula_communication.search.property_search import find_node_template_of_property
from nebula_communication.search.search_of_endpoint import search_of_endpoint_from_son
from nebula_communication.template_builder.definition.ServiceTemplateDefinition import \
    construct_service_template_definition
from nebula_communication.update_template.find_vertex import find_vertex
from nebula_communication.update_template.update_functions import is_service_status_exist, add_service_status, \
    set_service_status
from nebula_communication.update_template.update_template import update_template
from parser.linker.tosca_v_1_3.main_linker import main_linker
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import service_template_definition_parser


@app.route(f'/{cav}/yaml-template/<path:varargs>', methods=['POST'])
# curl -X POST -F file=@nebula_communication/jupyter.yaml  http://127.0.0.1:5000/yaml-template?cluster_name=Jupyter_3
def yaml_add(varargs=None):
    try:
        if varargs is None:
            return jsonify({'status': 400,
                            'message': 'what type are you uploading?'})
        varargs = varargs.split('/')
        if len(varargs) > 1:
            return jsonify({'status': 400,
                            'message': 'wrong url address'})
        if varargs[0] not in {'type', 'instance_model', 'template'}:
            return jsonify({'status': 400,
                            'message': 'was chosen incorrect type'})
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
                template.template_type = varargs[0]
                main_linker(template)
                if add_vid(template.name, template.name):
                    return jsonify({'status': 400,
                                    'message': f'cluster_name: {cluster_name} is taken'})
                if request.method == 'POST':
                    print('DEPLOY START')
                    deploy(template, template.name)
                print('DEPLOY FINISH')
                return jsonify({'status': 200,
                                'message': f'cluster_name: {cluster_name} was deployed'})
        return '''
                400 Bad Request 
                '''
    except HTTPException as e:
        return jsonify({'status': e.code,
                        'message': e.description})


@app.route(f'/{cav}/yaml-template', methods=['GET'])
def get_yaml():
    try:

        """
                 curl -X GET 'http://127.0.0.1:5000/yaml-template?cluster_name=Jupyter_3'
                :return:
                """
        cluster_name = request.args.get('cluster_name')
        only = request.args.get('only')
        if only not in {'attribute', 'property', None}:
            return jsonify({'status': 400,
                            'message': 'attribute "only" could be only attribute, property or None'})
        result = construct_service_template_definition(cluster_name, only)
        print(yaml.dump(result, default_flow_style=False))
        logging.info(yaml.dump(result, default_flow_style=False))
        return jsonify({'status': 200,
                        'message': result})
    except HTTPException as e:
        return jsonify({'status': e.code,
                        'message': e.description})


@app.route(f'/{cav}/cluster_names', methods=['GET'])
@app.route(f'/{cav}/cluster_names/<path:varargs>', methods=['GET', 'POST'])
def cluster_names(varargs=None):
    try:
        if varargs is None:
            vid = find_vertex_by_properties("ServiceTemplateDefinition")
            print(vid.column_values('id'))
            message = []
            for vid in vid.column_values('id'):
                message.append(vid.as_string())
            message = {'status': 200,
                       'cluster_names': message}
            message = jsonify(message)
            return message
            # return render_template("LIST_OF_cluster_names.html", cluster_names=vid.column_values('id'))
        else:
            varargs = varargs.split("/")
            if len(varargs) > 1:
                abort(400)
            result = fetch_vertex('"' + varargs[0] + '"', "ServiceTemplateDefinition")
            if result is None:
                result = False
            else:
                result = True
            if request.method == 'POST':
                cluster_name = '"' + varargs[0] + '"'
                delete_cluster(cluster_name)
                return jsonify({'status': 200,
                                'message': f'cluster: {cluster_name} was deleted'})
            else:
                message = jsonify({'status': 200,
                                   'message': result})
                return message
    except HTTPException as e:
        return jsonify({'status': e.code,
                        'message': e.description})


@app.route(f'/{cav}/yaml-template/<path:varargs>', methods=['PATCH'])
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


@app.route(f'/{cav}/yaml_delete_all', methods=['PATCH'])
# curl -X PATCH http://127.0.0.1:5000/yaml-delete
def yaml_delete_all():
    delete_all()
    return "200 OK"


@app.route(f'/{cav}/find/<path:varargs>', methods=['GET'])
def find(varargs=None):
    search_by = request.args.get('search_by')
    search_by_value = request.args.get('search_by_value')
    cluster_name = request.args.get('cluster_name')
    vertex_type_system = request.args.get('vertex_type_system')
    find_cluster_name = request.args.get('find_cluster_name')
    node_vid = request.args.get('node_vid')
    requirement_name = request.args.get('requirement_name')
    result = find_vertex(cluster_name, vertex_type_system)
    return "200 OK"


@app.route(f'/{cav}/get_endpoint_of_service', methods=['GET'])
def get_endpoint_of_service(find_free=False):
    """
         curl -X GET 'http://127.0.0.1:5000/get_endpoint_of_service?type_of_service=michman.nodes.Jupyter.Jupyter-6-0-1'
    :return:
    """
    cluster_name = request.args.get('cluster_name')
    type_of_service = request.args.get('type_of_service')
    if not type_of_service:
        abort(400)
    result = search_of_endpoint_from_son(type_of_service, cluster_name, find_free=find_free)
    print(yaml.dump(result, default_flow_style=False))
    return result


@app.route(f'/{cav}/get_free_endpoint_of_service', methods=['GET'])
def get_free_endpoint_of_service():
    """
         curl -X GET 'http://127.0.0.1:5000/get_free_endpoint_of_service?type_of_service=michman.nodes.Jupyter.Jupyter-6-0-1'
    :return:
    """
    return get_endpoint_of_service(find_free=True)


@app.route(f'/{cav}/set_service_free', methods=['PATCH'])
def set_service_free(status='free'):
    """
        curl -X PATCH "http://127.0.0.1:5000/set_service_busy?cluster_name=Jupyter_1&service_name=jupyter_1"

    :return:
    """
    cluster_name = request.args.get('cluster_name')
    service_name = request.args.get('service_name')
    if not cluster_name or not service_name:
        abort(400)
    flag = is_service_status_exist(cluster_name, service_name)
    if not flag:
        add_service_status(cluster_name, service_name)
    set_service_status(cluster_name, service_name, status=status)
    return 'OK'


@app.route(f'/{cav}/set_service_busy', methods=['PATCH'])
def set_service_busy():
    return set_service_free(status='busy')


@app.route(f'/{cav}/find_node_with_property', methods=['GET'])
def find_node_with_property():
    """
     curl -X GET "http://127.0.0.1:5000/find_node_with_property?values=256%20GB&cluster_name=Jupyter_1"
    :return:
    """
    kwargs = request.args
    result = find_node_template_of_property(**(kwargs.to_dict()))
    return result


@app.route(f'/{cav}/find_node_with_mutual_properties', methods=['GET'])
def find_node_with_mutual_property():
    kwargs = request.args
    """
     curl -X GET "http://127.0.0.1:5000/find_node_with_mutual_properties?values_1=256%20GB&cluster_name=Jupyter_1"
    """
    result = {}
    dict_to_operate = {}
    for key, value in kwargs.items():
        digit = key.split("_")
        if digit[-1].isdigit():
            if dict_to_operate.get(digit[-1]):
                dict_to_operate[digit[-1]] = dict_to_operate[digit[-1]] | ({'_'.join(digit[:-1]): value})
            else:
                dict_to_operate[digit[-1]] = {'_'.join(digit[:-1]): value}
                if kwargs.get('cluster_name'):
                    dict_to_operate[digit[-1]] = dict_to_operate[digit[-1]] | {
                        'cluster_name': kwargs.get('cluster_name')}
            kwargs.get('cluster_name')

    print(yaml.dump(dict_to_operate, default_flow_style=False))
    fl = list(dict_to_operate.values())
    result = find_node_template_of_property(**fl[0])
    for value in fl[1:]:
        new_result = find_node_template_of_property(**value)
        if result == {} or new_result == {}:
            return {}
        tmp_answer = {}
        for key, values in result.items():
            for key_2, values_2 in new_result.items():
                if key_2 == key and values_2.keys() & values.keys():
                    tmp_result = {}
                    for key_tmp in values_2.keys() & values.keys():
                        tmp_result = tmp_result | {key_tmp: values_2.get(key_tmp)}
                    tmp_answer = tmp_answer | {key_2: tmp_result}
        result = tmp_answer
    return result
