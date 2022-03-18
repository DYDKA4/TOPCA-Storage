from flask import request
from app import app
from app import communication_with_nebula
from app import yaml_parser
import yaml
from app import constructor_yaml


@app.route('/yaml-template/', methods=['POST', 'PUT', 'GET'])
@app.route('/yaml-template/<path:varargs>', methods=['PATCH'])
# curl -F file=@jamlExamples/SBS.yaml http://127.0.0.1:5000/yaml-template?cluster_name="cluster"
def yaml_add(varargs=None):
    cluster_name = request.args.get('cluster_name')
    if request.method in ['POST','PUT']:
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
        curl -X PATCH 
        Поддерживаемые пути: 
        'http://127.0.0.1:5000/yaml-template/topology_template/relationship_templates/*template_name*/type?cluster_
        name=*new_value*'

        '''
        print(varargs, cluster_name)
        varargs = varargs.split("/")
        new_value = request.args.get('new_value')
        pure_yaml = communication_with_nebula.get_yaml_from_cluster(cluster_name)
        if pure_yaml is None:
            return '400 Bad Request'
        pure_yaml = yaml.safe_load(pure_yaml)
        data = pure_yaml
        print(pure_yaml)
        # поиск нужного ключа в yaml шаблоне и замена его
        for i, key in enumerate(varargs):
            if data.get(key):
                print(type(data[key]), data[key])
                data = data[key]
                if i == len(varargs) - 2:
                    if data.get(varargs[i + 1]):
                        print(type(data[varargs[i + 1]]), data[varargs[i + 1]])
                        # data[varargs[i + 1]] = {'location': '/some_other_data_location_2'}
                        data[varargs[i + 1]] = new_value
                        print(type(data[varargs[i + 1]]), data[varargs[i + 1]])
                        break
                    else:
                        return '400 Bad Path'
            else:
                return '400 Bad Path'
        print(pure_yaml)
        communication_with_nebula.update_vertex(None, 'ClusterName', 'pure_yaml',
                                                '"' + str(pure_yaml) + '"', f'"{cluster_name}"',
                                                start_session=True)
        if varargs[0] == 'topology_template':
            # работаем с assignment частью
            if varargs[1] == 'relationship_templates':
                # работаем с relationship_templates
                vid_of_template = communication_with_nebula. \
                    find_destination_by_property(None, f'"{cluster_name}"', 'assignment', 'name',
                                                 varargs[2], start_session=True)
                if varargs[3] == 'type':
                    # изменение типа

                    return '501 CHANGE TYPE'
                elif varargs[3] == 'properties':
                    '''
                    curl -X PATCH 'http://127.0.0.1:5000/yaml-template/topology_template/relationship_templates/
                    storage_attachesto_1/properties/location?cluster_name=cluster_tosca_58&new_value=/data_location_2'
                    '''
                    definition_property = communication_with_nebula. \
                        find_destination_by_property(None, f'"{vid_of_template}"', 'definition_property', 'value_name',
                                                     varargs[4], start_session=True)
                    communication_with_nebula.update_vertex(None, 'DefinitionProperties', 'values',
                                                            f'"{new_value}"', f'"{definition_property}"',
                                                            start_session=True)
                    return '200 OK Change properties'
                else:
                    return '400 Bad'
            elif varargs[1] == 'node_templates':
                # работаем с node
                vid_of_node = communication_with_nebula. \
                    find_destination_by_property(None, f'"{cluster_name}"', 'assignment', 'name',
                                                 varargs[2], start_session=True)
                print(vid_of_node)
                if varargs[3] == 'type':
                    # изменение типа
                    return '501 Not Implemented'
                elif varargs[3] == 'capabilities':
                    '''
                    'http://127.0.0.1:5000/yaml-template/topology_template/node_templates/my_web_app_tier_2/
                    capabilities/host/properties/disk_size?cluster_name=cluster_tosca_58&new_value=70%20GB'
                    '''
                    # изменение capabilities:
                    vid_of_capability = communication_with_nebula. \
                        find_destination_by_property(None, f'"{vid_of_node}"', 'assignment_capability', 'name',
                                                     varargs[4], start_session=True)
                    if varargs[5] == 'properties':
                        assignment_property = communication_with_nebula.\
                            find_destination_by_property(None, f'"{vid_of_capability}"', 'assignment_property',
                                                         'value_name', varargs[6], start_session=True)
                        communication_with_nebula.update_vertex(None, 'AssignmentProperties', 'values',
                                                                f'"{new_value}"', f'"{assignment_property}"',
                                                                start_session=True)
                        return '200 OK Change of capability'
                    return '400 Fail'
                elif varargs[3] == 'requirements':
                    # изменение requirements
                    return '501 Not Implemented'
                elif varargs[3] == 'properties':
                    # изменение properties
                    '''
                    curl -X PATCH 'http://127.0.0.1:5000/yaml-template/topology_template/node_templates/my_storage/
                    properties/size?cluster_name=cluster_tosca_58&new_value=40%20GB'
                    '''
                    assignment_property = communication_with_nebula. \
                        find_destination_by_property(None, f'"{vid_of_node}"', 'assignment_property', 'value_name',
                                                     varargs[4], start_session=True)
                    communication_with_nebula.update_vertex(None, 'AssignmentProperties', 'values',
                                                            f'"{new_value}"', f'"{assignment_property}"',
                                                            start_session=True)

                    return '100 OK Change properties'
                return '501 Not Implemented'
        elif varargs[0] == 'node_types':
            #работаем с node_types
            vid_of_node = communication_with_nebula. \
                find_destination_by_property(None, f'"{cluster_name}"', 'definition', 'vertex_type_tosca',
                                             varargs[1], start_session=True)
            print(vid_of_node)
            if varargs[2] == 'properties':
                """
                curl -X PATCH 'http://127.0.0.1:5000/yaml-template/node_types/tosca.nodes.Root/properties/
                tosca_id/type?cluster_name=cluster_tosca_59&new_value=NaN'
                """
                assignment_property = communication_with_nebula. \
                    find_destination_by_property(None, f'"{vid_of_node}"', 'definition_property', 'value_name',
                                                 varargs[4], start_session=True, edge_property_value=varargs[3],
                                                 edge_property_name='name')
                print(assignment_property)
                communication_with_nebula.update_vertex(None, 'DefinitionProperties', 'values',
                                                        f'"{new_value}"', f'"{assignment_property}"',
                                                        start_session=True)
                return '100 OK Change properties in definition_node'
            else:
                return '501 Not Implemented'
        elif varargs[0] == 'capability_types':
            #работаем с capability_types
            vid_of_node = communication_with_nebula. \
                find_destination_by_property(None, f'"{cluster_name}"', 'definition', 'vertex_type_tosca',
                                             varargs[1], start_session=True)
            print(vid_of_node)
            if varargs[2] == 'properties':
                assignment_property = communication_with_nebula. \
                    find_destination_by_property(None, f'"{vid_of_node}"', 'definition_property', 'value_name',
                                                 varargs[4], start_session=True, edge_property_value=varargs[3],
                                                 edge_property_name='name')
                print(assignment_property)
                communication_with_nebula.update_vertex(None, 'DefinitionProperties', 'values',
                                                        f'"{new_value}"', f'"{assignment_property}"',
                                                        start_session=True)
                return '100 OK Change properties in capability_types'
            else:
                return '501 Not Implemented'
        elif varargs[0] == 'relationship_types':
            #работаем с capability_types
            vid_of_node = communication_with_nebula. \
                find_destination_by_property(None, f'"{cluster_name}"', 'definition', 'vertex_type_tosca',
                                             varargs[1], start_session=True)
            print(vid_of_node)
            if varargs[2] == 'properties':
                assignment_property = communication_with_nebula. \
                    find_destination_by_property(None, f'"{vid_of_node}"', 'definition_property', 'value_name',
                                                 varargs[4], start_session=True, edge_property_value=varargs[3],
                                                 edge_property_name='name')
                print(assignment_property)
                communication_with_nebula.update_vertex(None, 'DefinitionProperties', 'values',
                                                        f'"{new_value}"', f'"{assignment_property}"',
                                                        start_session=True)
                return '100 OK Change properties in relationship_types'
            else:
                return '501 Not Implemented'
        else:
            return '501 Not Implemented'

        return f'{varargs} {cluster_name} {new_value}\n{data}'
    if request.method == 'GET':
        """
        curl -X GET 'http://127.0.0.1:5000/yaml-template/?cluster_name=cluster_tosca_59'
        """
        yaml_collection = constructor_yaml.get_yaml(cluster_name)

        return f'{yaml_collection}'

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
