import yaml

from werkzeug.exceptions import abort


from random import choice
from string import ascii_uppercase

from nebula_communication.nebula_functions import add_in_vertex, vid_getter, add_edge
from parser.linker.tosca_v_1_3.main_linker import main_linker
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import service_template_definition_parser


def deploy(template) -> None:
    name_of_key_value = ''
    key_value = ''
    complex_vertex = {}
    if type(template) == str:
        print(template)
    if template.vid is None or template.vertex_type_system == 'ServiceTemplateDefinition':
        for attribute_name, attribute_value in template.__dict__.items():
            if type(attribute_value) in {int, float, str, bool} and attribute_name not in {'vid'}:
                if name_of_key_value == '':
                    if attribute_value is not None:
                        name_of_key_value = attribute_name
                        key_value = '"' + str(attribute_value) + '"'
                else:
                    if attribute_value is not None:
                        name_of_key_value = name_of_key_value + ", " + attribute_name
                        key_value = key_value + ', "' + str(attribute_value) + '"'
            elif attribute_name not in {'vid', 'vertex_type_system'} and attribute_value is not None:
                complex_vertex[attribute_name] = attribute_value
        if template.vid is None:
            template.vid = vid_getter(template.vertex_type_system)
        # print(template.__dict__)


        add_in_vertex(template.vertex_type_system, name_of_key_value, key_value, template.vid)
    # for edge in edges:
    #     add_edge(edge[0], edge[1], edge[2].vid, edge[3].vid, edge[4]) # todo Thing about it
    for attribute_name, attribute_value in complex_vertex.items():
        if type(attribute_value) == list:
            for attribute_item in attribute_value:
                # if attribute_item.vertex_type_system in realised_vertex_type:  # todo Remove when it will be done
                    deploy(attribute_item)
                    # edges.append([attribute_name, '', template, attribute_item, ''])
                    if attribute_name == 'steps':
                        attribute_name = 'steps_tosca'
                    add_edge(attribute_name, '', template.vid, attribute_item.vid, '')
        elif type(attribute_value) == dict:
            for type_edge, vertexes in attribute_value.items():
                # edges.append([type_edge, '', vertexes[0], vertexes[1], ''])
                if type(vertexes) == dict:
                    abort(400)
                elif type(vertexes) == list:
                    if len(vertexes) == 0:
                        print(vertexes)
                    # if template.vertex_type_system == 'ConditionClauseDefinition':

                    if vertexes:
                        if type(vertexes[0]) == list and type(vertexes[1]) == list:
                            for vertex_0 in vertexes[0]:
                                for vertex_1 in vertexes[1]:
                                    if vertex_0.vid is None:
                                        deploy(vertex_0)
                                    if vertex_1.vid is None:
                                        deploy(vertex_1)
                                    if attribute_name == 'steps':
                                        attribute_name = 'steps_tosca'
                                    add_edge(type_edge, '', vertex_0.vid, vertex_1.vid, '')
                        elif type(vertexes[0]) == list:
                            for vertex in vertexes[0]:
                                if vertexes[1].vid is None:
                                    deploy(vertexes[1])
                                if vertex.vid is None:
                                    deploy(vertex)
                                if attribute_name == 'steps':
                                    attribute_name = 'steps_tosca'
                                add_edge(type_edge, '', vertex.vid, vertexes[1].vid, '')
                        elif type(vertexes[1]) == list:
                            for vertex in vertexes[1]:
                                if vertexes[0].vid is None:
                                    deploy(vertex[0])
                                if vertex.vid is None:
                                    deploy(vertex)
                                if attribute_name == 'steps':
                                    attribute_name = 'steps_tosca'
                                add_edge(type_edge, '', vertexes[0].vid, vertex.vid, '')
                        else:
                            if vertexes[0].vid is None:
                                deploy(vertexes[0])
                            if vertexes[1].vid is None:
                                deploy(vertexes[1])
                            if attribute_name == 'steps':
                                attribute_name = 'steps_tosca'
                            add_edge(type_edge, '', vertexes[0].vid, vertexes[1].vid, '')
        else:
            deploy(attribute_value)
            if attribute_name == 'steps':
                attribute_name = 'steps_tosca'
            add_edge(attribute_name, '', template.vid, attribute_value.vid, '')

    return


file = open('service_template.yaml')
data = file.read()
file.close()
data = yaml.safe_load(data)
template = service_template_definition_parser(''.join(choice(ascii_uppercase) for i in range(12)), data)
main_linker(template)
# template
deploy(template)
