from flask import request
from app import app
from app import communication_with_nebula
from app import yaml_parser
import yaml


@app.route('/yaml-template', methods=['POST'])
# curl -F file=@jamlExamples/SBS.yaml http://127.0.0.1:5000/yaml-template?cluster_name="cluster"
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
    print(pure_yaml)
    cluster_name = request.args.get('cluster_name')
    if cluster_name:
        cluster_vertex = yaml_parser.parser(file, cluster_name)
        cluster_vertex.pure_yaml = pure_yaml
        end_code = '400'
        end_code = communication_with_nebula.yaml_deploy(cluster_vertex)
        print()
        return f'{end_code}'
    return '''
            400 Bad Request 
            '''

