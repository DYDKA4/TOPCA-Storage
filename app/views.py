from flask import request
from app import app
from datetime import datetime
from app import communication_with_nebula
# from app import json_parser
from app import yaml_parser
import json
import yaml


@app.route('/yaml-template', methods=['POST'])
def yaml_add():
    file = request.files['file']
    if file:
        file = file.read().decode("utf-8")
        file = yaml.safe_load(file)
        pure_yaml = file
    else:
        return '''
        400 Bad Request 
        '''

    cluster_name = request.args.get('cluster_name')
    if cluster_name:
        data_assignments, node_types, capability_types = yaml_parser.parser(file)
        # for i in data_assignments:
        #     print(i)
        # print('\nnode_types')
        # for i in node_types:
        #     print(i)
        # print('\ncapability_types')
        # for i in capability_types:
        #     print(i)
        # print(cluster_name)
        end_code = '400'
        # end_code = communication_with_nebula.yaml_deploy(data_assignments, node_types, capability_types, cluster_name,
        #                                                  pure_yaml)
        print()
        return f'{end_code}'
    return '''
            400 Bad Request 
            '''


# @app.route('/json-template', methods=['POST'])
# def json_add():
#     json_results = request.get_json(force=True)
#     data = json_parser.parser(json_results)
#     print(data)
#     communication_with_nebula.yaml_deploy(data)
#     print()
#     return '''
#               OK'''


@app.route('/server-add', methods=['GET', 'POST'])
def server_add():
    # if key doesn't exist, returns a 400, bad request error
    print(request.method)
    cpu = request.args.get('cpu')
    # if key doesn't exist, returns a 400, bad request error
    ram = request.args.get('ram')

    # if key doesn't exist, returns None
    mem = request.args.get('mem')

    # some tests with json from file
    json_results = request.get_json(force=True)
    print(json_results)

    owner = request.args.get('owner')
    print(cpu, ram, mem, owner)
    date = str(datetime.now())

    if request.method == 'POST':
        communication_with_nebula.add_server(cpu, ram, mem, owner, date)
    elif request.method == 'GET':
        result = communication_with_nebula.find_server(cpu, ram, mem, owner)
        if not result:
            return 'NULL'
        print(json.dumps(result))
        return json.dumps(result)
    # template of usage: http://127.0.0.1:5000/server-add?cpu=4&ram=4&mem=50&owner=Tulin.D.I
    return '''
              <h1>The cpu value is: {}</h1>
              <h1>The ram value is: {}</h1>
              <h1>The mem value is: {}</h1>
              <h1>The owner value is: {}</h1>
                  <h1>The date value is: {}'''.format(cpu, ram, mem, owner, date)


@app.route('/query-example')
def query_example():
    # http://127.0.0.1:5000/query-example?language=Python&framework=Flask&website=DigitalOcean
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)


@app.route('/', methods=['GET', 'POST'])
def test():
    print(request.method)
    name = request.args['name']
    print(name)
    return 'asd'
