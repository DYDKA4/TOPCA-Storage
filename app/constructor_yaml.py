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


def form_properties(list_of_properties, definition_flag=False, name_in_edge=False, source_vid=None):
    properties = {}
    for properties_vid in list_of_properties:
        properties_vid = properties_vid.as_string()
        if definition_flag:
            vertex_type = 'DefinitionProperties'
            edge_type = 'definition_property'
        else:
            vertex_type = 'AssignmentProperties'
            edge_type = 'assignment_property'
        value_name = cwn.fetch_vertex(None, f'"{properties_vid}"', vertex_type,
                                      'value_name', start_session=True)
        values = cwn.fetch_vertex(None, f'"{properties_vid}"', vertex_type,
                                  'values', start_session=True)
        try:
            values = ast.literal_eval(values)
        except ValueError:
            pass
        except SyntaxError:
            pass

        if name_in_edge:
            name = cwn.fetch_edge(None, f'"{source_vid}"', f'"{properties_vid}"', edge_type, 'name',
                                  start_session=True)
            deep_update_dict(properties, {name: {value_name: values}})
        else:
            deep_update_dict(properties, {value_name: values})
    properties = {'properties': properties}
    return properties


def form_capabilities(list_of_capability, definition_flag=False, name_in_edge=False,
                      source_vid=None, flag_form_properties=True):
    capabilities = {}
    for capabilities_vid in list_of_capability:
        capabilities_vid = capabilities_vid.as_string()
        if definition_flag:
            vertex_type = 'DefinitionCapabilities'
            edge_type = 'definition_capability'
            property_edge = 'definition_property'
            column = 'vertex_type_tosca'
        else:
            vertex_type = 'AssignmentCapabilities'
            edge_type = 'assignment_capability'
            property_edge = 'assignment_property'
            column = 'name'
        capabilities_name = cwn.fetch_vertex(None, f'"{capabilities_vid}"', vertex_type,
                                             column, start_session=True)
        if name_in_edge:
            name = cwn.fetch_edge(None, f'"{source_vid}"', f'"{capabilities_vid}"', edge_type, 'name',
                                  start_session=True)
            deep_update_dict(capabilities, {name: {'type': capabilities_name}})

        elif flag_form_properties:
            capabilities_property_list = cwn.find_destination(None, f'"{capabilities_vid}"',
                                                              property_edge, start_session=True,
                                                              full_list=True)
            capabilities_property = form_properties(capabilities_property_list)
            capabilities = deep_update_dict(capabilities, {capabilities_name: capabilities_property})
        else:
            capabilities = deep_update_dict(capabilities, capabilities_name)
    if capabilities:
        capabilities = {'capabilities': capabilities}
    else:
        return {}
    return capabilities


def form_requirements(list_of_requirements, definition_flag=False):
    list_of_requirements_ready = []
    if definition_flag:
        vertex_type = 'DefinitionVertex'
        column = 'vertex_type_tosca'
        relationship = 'RelationshipType'
    else:
        vertex_type = 'AssignmentVertex'
        column = 'name'
        relationship = 'RelationshipTemplate'
    for requirement_vid in list_of_requirements:
        requirement_vid = requirement_vid.as_string()
        requirement_name = cwn.fetch_vertex(None, f'"{requirement_vid}"', 'RequirementsVertex',
                                            'name', start_session=True)
        requirement_destination = cwn.find_destination(None, f'"{requirement_vid}"',
                                                       'requirements_destination', start_session=True)
        destination_name = cwn.fetch_vertex(None, f'"{requirement_destination}"', vertex_type,
                                            column, start_session=True)
        occurrences = cwn.fetch_vertex(None, f'"{requirement_vid}"', 'RequirementsVertex',
                                       'occurrences', start_session=True)
        if occurrences:
            occurrences = ast.literal_eval(occurrences)

        requirement_capability = cwn.find_destination(None, f'"{requirement_vid}"',
                                                      'requirements_capability', start_session=True)
        requirement_capability_name = None
        print(requirement_capability)
        if requirement_capability:
            requirement_capability_name = cwn.fetch_vertex(None, f'"{requirement_capability}"',
                                                           'DefinitionCapabilities',
                                                           column, start_session=True)
        requirement_template = cwn.find_destination(None, f'"{requirement_vid}"',
                                                    'requirements', start_session=True)
        template_name = cwn.fetch_vertex(None, f'"{requirement_template}"', relationship,
                                         column, start_session=True)

        requirement = ({requirement_name: {'node': destination_name,
                                           'relationship': template_name}})
        if requirement_capability:
            deep_update_dict(requirement[requirement_name], {'capability': requirement_capability_name})
        if occurrences:
            deep_update_dict(requirement[requirement_name], {'occurrences': occurrences})
        list_of_requirements_ready.append(requirement)

    list_of_requirements_ready = {'requirements': list_of_requirements_ready}
    return list_of_requirements_ready


def get_yaml(cluster_name):
    """
    Обработка defention части
    :return:
    """
    nodes_template_assignment = {}
    nodes_template_definition = {}
    relationship_templates = {}
    assignment = cwn.find_destination(None, f'"{cluster_name}"', 'assignment', start_session=True, full_list=True)
    for vid in assignment:
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
            list_of_requirements_ready = form_requirements(list_of_requirements)
            list_of_requirements_ready = {'requirements': list_of_requirements_ready}
            if list_of_requirements_ready.get('requirements'):
                deep_update_dict(node_template[name], list_of_requirements_ready)
            capabilities = form_capabilities(list_of_capability)
            if capabilities.get('capabilities'):
                deep_update_dict(node_template[name], capabilities)
            properties = form_properties(list_of_properties)
            if properties.get('properties'):
                deep_update_dict(node_template[name], properties)
            deep_update_dict(nodes_template_assignment, node_template)

        elif 'RelationshipTemplate' in vid:
            print('Template')
            relationship_template = {}
            name = cwn.fetch_vertex(None, f'"{vid}"', 'RelationshipTemplate', 'name', start_session=True)
            type_relationship_vid = cwn.find_destination(None, f'"{vid}"', 'type_relationship', start_session=True)
            type_relationship_name = cwn.fetch_vertex(None, f'"{type_relationship_vid}"',
                                                      'RelationshipType', 'vertex_type_tosca', start_session=True)
            list_of_properties = cwn.find_destination(None, f'"{vid}"',
                                                      'definition_property', start_session=True, full_list=True)
            properties = form_properties(list_of_properties, definition_flag=True)
            relationship_template = {name: {'type': type_relationship_name}}
            if properties.get('properties'):
                deep_update_dict(relationship_template[name], properties)
            deep_update_dict(relationship_templates, relationship_template)

        else:
            return None
    definition = cwn.find_destination(None, f'"{cluster_name}"', 'definition', start_session=True, full_list=True)
    for vid in definition:
        vid = vid.as_string()
        if 'DefinitionVertex' in vid:
            vertex_type_tosca = cwn.fetch_vertex(None, f'"{vid}"', 'DefinitionVertex',
                                                 'vertex_type_tosca', start_session=True)
            list_of_properties = cwn.find_destination(None, f'"{vid}"',
                                                      'definition_property', start_session=True, full_list=True)
            list_of_capability = cwn.find_destination(None, f'"{vid}"',
                                                      'definition_capability', start_session=True, full_list=True)
            list_of_requirements = cwn.find_destination(None, f'"{vid}"',
                                                        'requirements', start_session=True, full_list=True)
            derived_from_vid = cwn.find_destination(None, f'"{vid}"',
                                                    'derived_from', start_session=True)
            properties = form_properties(list_of_properties, definition_flag=True, name_in_edge=True, source_vid=vid)
            capabilities = form_capabilities(list_of_capability, definition_flag=True, name_in_edge=True,
                                             source_vid=vid)
            list_of_requirements_ready = form_requirements(list_of_requirements, definition_flag=True)

            node_template = vertex_type_tosca
            if derived_from_vid:
                derived_from = cwn.fetch_vertex(None, f'"{derived_from_vid}"',
                                                'DefinitionVertex', 'vertex_type_tosca', start_session=True)
                deep_update_dict(nodes_template_definition, {node_template: {'derived_from': derived_from}})
            if capabilities.get('capabilities'):
                deep_update_dict(nodes_template_definition, {node_template: capabilities})
            if properties.get('properties'):
                deep_update_dict(nodes_template_definition, {node_template: properties})
            if list_of_requirements_ready.get('requirements'):
                deep_update_dict(nodes_template_definition, {node_template: list_of_requirements_ready})
            if not (capabilities.get('capabilities') or properties.get('properties') or
                    list_of_requirements_ready.get('requirements')):
                deep_update_dict(nodes_template_definition, {node_template: 'None'})
    if nodes_template_definition:
        nodes_template_definition = {'node_types': nodes_template_definition}
    if nodes_template_assignment:
        nodes_template_assignment = {'node_templates': nodes_template_assignment}
    if relationship_templates:
        relationship_templates = {'relationship_templates': relationship_templates}
        deep_update_dict(nodes_template_assignment, relationship_templates)

    template = nodes_template_definition
    deep_update_dict(template, {'topology_template': nodes_template_assignment})
    with open('./output.yaml', 'w') as file:
        documents = yaml.dump(template, file)
    return template
