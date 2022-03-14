from app import communication_with_nebula as cwn
import itertools
import yaml
import ast
import json
import pprint


def deep_update_dict(source, overrides):
    assert isinstance(source, dict)
    assert isinstance(overrides, dict)

    for k, v in overrides.items():
        if isinstance(v, dict) and isinstance(source.get(k), dict):
            source[k] = deep_update_dict(source.get(k, {}), v)
        elif isinstance(v, (list, set, tuple)) and isinstance(source.get(k), type(v)):
            type_save = type(v)
            source[k] = type_save(itertools.chain(iter(source[k]), iter(v)))
        else:
            source[k] = v
    return source


def form_properties(list_of_properties):
    properties = {}
    for properties_vid in list_of_properties:
        properties_vid = properties_vid.as_string()
        value_name = cwn.fetch_vertex(None, f'"{properties_vid}"', 'AssignmentProperties',
                                      'value_name', start_session=True)
        values = cwn.fetch_vertex(None, f'"{properties_vid}"', 'AssignmentProperties',
                                  'values', start_session=True)
        try:
            values = ast.literal_eval(values)
        except ValueError:
            pass
        except SyntaxError:
            pass
        deep_update_dict(properties, {value_name: values})
    properties = {'properties': properties}
    return properties


def form_capabilities(list_of_capability):
    capabilities = {}
    for capabilities_vid in list_of_capability:
        capabilities_vid = capabilities_vid.as_string()

        capabilities_name = cwn.fetch_vertex(None, f'"{capabilities_vid}"', 'AssignmentCapabilities',
                                             'name', start_session=True)
        capabilities_property_list = cwn.find_destination(None, f'"{capabilities_vid}"',
                                                          'assignment_property', start_session=True,
                                                          full_list=True)
        capabilities_property = form_properties(capabilities_property_list)

        capabilities = deep_update_dict(capabilities, {capabilities_name: capabilities_property})
    capabilities = {'capabilities': capabilities}
    return capabilities


def get_yaml(cluster_name):
    """
    Обработка defention части
    :return:
    """
    nodes_template = {}
    result = cwn.find_destination(None, f'"{cluster_name}"', 'assignment', start_session=True, full_list=True)
    for vid in result:
        vid = vid.as_string()
        if 'AssignmentVertex' in vid:
            name = cwn.fetch_vertex(None, f'"{vid}"', 'AssignmentVertex', 'name', start_session=True)
            type_of_vertex = cwn.fetch_vertex(None, f'"{vid}"', 'AssignmentVertex', 'type', start_session=True)
            node_template = {name: {'type': type_of_vertex}}
            list_of_properties = cwn.find_destination(None, f'"{vid}"',
                                                      'assignment_property', start_session=True, full_list=True)
            list_of_capability = cwn.find_destination(None, f'"{vid}"',
                                                      'assignment_capability', start_session=True, full_list=True)
            list_of_requirements = cwn.find_destination(None, f'"{vid}"',
                                                        'requirements', start_session=True, full_list=True)
            list_of_requirements_ready = []
            for requirement_vid in list_of_requirements:
                requirement_vid = requirement_vid.as_string()
                requirement_name = cwn.fetch_vertex(None, f'"{requirement_vid}"', 'RequirementsVertex',
                                                    'name', start_session=True)
                requirement_destination = cwn.find_destination(None, f'"{requirement_vid}"',
                                                               'requirements_destination', start_session=True,
                                                               full_list=True)
                requirement_destination = requirement_destination[0].as_string()
                destination_name = cwn.fetch_vertex(None, f'"{requirement_destination}"', 'AssignmentVertex',
                                                    'name', start_session=True)

                requirement_template = cwn.find_destination(None, f'"{requirement_vid}"',
                                                            'requirements', start_session=True,
                                                            full_list=True)
                requirement_template = requirement_template[0].as_string()
                template_name = cwn.fetch_vertex(None, f'"{requirement_template}"', 'RelationshipTemplate',
                                                 'name', start_session=True)
                list_of_requirements_ready.append({requirement_name: {'node': destination_name,
                                                                      'relationship': template_name}})

            list_of_requirements_ready = {'requirements': list_of_requirements_ready}
            if list_of_requirements_ready.get('requirements'):
                deep_update_dict(node_template[name], list_of_requirements_ready)
            capabilities = form_capabilities(list_of_capability)
            if capabilities.get('capabilities'):
                deep_update_dict(node_template[name], capabilities)
            properties = form_properties(list_of_properties)
            if properties.get('properties'):
                deep_update_dict(node_template[name], properties)
            deep_update_dict(nodes_template, node_template)

        elif 'RelationshipTemplate' in vid:
            print('Template')
        else:
            return None
    nodes_template = {'node_templates': nodes_template}
    with open('./output.yaml', 'w') as file:
        documents = yaml.dump(nodes_template, file)
    return nodes_template
