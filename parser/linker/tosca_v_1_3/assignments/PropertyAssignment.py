import json

from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment
from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import ParameterDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


def set_get_property(property_assignment: PropertyAssignment, destination_property_assignment: PropertyAssignment):
    if property_assignment.vertex_type_system != 'PropertyAssignment':
        abort(400)
    if type(property_assignment.get_property) == dict:
        vertexes = property_assignment.get_property.get('get_property')
        new_destination: list = vertexes[1]
        new_destination.append(destination_property_assignment)
        property_assignment.get_property = {'get_property': [property_assignment,
                                                             new_destination]}
    else:
        property_assignment.get_property = {'get_property': [property_assignment,
                                                             [destination_property_assignment]]}
    if type(property_assignment.value) == dict:
        property_assignment.value = json.dumps(property_assignment.value)
    return


def find_in_property_list(property_assignment: PropertyAssignment, destination_property_assignment_list: list,
                          value: str):
    for destination_property_assignment in destination_property_assignment_list:
        destination_property_assignment: PropertyAssignment
        if destination_property_assignment.name == value:
            set_get_property(property_assignment, destination_property_assignment)
            return True
    return False


def find_parent_template(template_definition: TemplateDefinition, property_assignment):
    for node_template in template_definition.node_templates:
        node_template: NodeTemplate
        for property_assignment_copy in node_template.properties:
            property_assignment_copy: PropertyAssignment
            if property_assignment_copy == property_assignment:
                return node_template
        for capability_assignment in node_template.capabilities:
            capability_assignment: CapabilityAssignment
            for property_assignment_copy in capability_assignment.properties:
                if property_assignment_copy == property_assignment:
                    return node_template
    return None


def find_parent_relationship_template(template_definition: TemplateDefinition, property_assignment):
    for relationship_template in template_definition.relationship_templates:
        relationship_template: RelationshipTemplate
        for property_assignment_copy in relationship_template.properties:
            property_assignment_copy: PropertyAssignment
            if property_assignment_copy == property_assignment:
                return relationship_template
    return None


def find_in_node_template_list(node_templates: list, target_name, value, property_assignment):
    for node_template in node_templates:
        node_template: NodeTemplate
        if node_template.name == target_name:
            if find_in_property_list(property_assignment, node_template.properties, value[0]):
                return True
            if len(value) > 1:
                for interface in node_template.interfaces:
                    interface: InterfaceDefinition
                    if interface.name == value[0]:
                        if find_in_property_list(property_assignment, interface.inputs, value[1]):
                            return True
                for requirement_assignment in node_template.requirements:
                    requirement_assignment: RequirementAssignment
                    if requirement_assignment.name == value[0]:
                        if find_in_property_list(property_assignment, requirement_assignment.properties, value[1]):
                            return True
                for capability_assignment in node_template.capabilities:
                    capability_assignment: CapabilityAssignment
                    if capability_assignment.name == value[0]:
                        if find_in_property_list(property_assignment, capability_assignment.properties, value[1]):
                            return True
    return False


def link_property_assignment(service_template: ServiceTemplateDefinition,
                             property_assignment: PropertyAssignment) -> None:
    template_definition: TemplateDefinition = service_template.topology_template
    if type(property_assignment.value) == dict:
        value = property_assignment.value
    else:
        return
    if value.get('get_property'):
        value = value.get('get_property')
        target_name = ''
        target_names = []
        if value[0] == 'SELF':
            parent_template: NodeTemplate = find_parent_template(template_definition, property_assignment)
            if parent_template is not None:
                value = value[1:]
                target_name = parent_template.name
            else:
                parent_template: RelationshipTemplate = find_parent_relationship_template(template_definition,
                                                                                          property_assignment)
                if parent_template is None:
                    abort(400)
                value = value[1:]
                target_name = parent_template.name

        elif value[0] == 'SOURCE':
            parent_relationship_template = find_parent_relationship_template(template_definition, property_assignment)
            for node_template in template_definition.node_templates:
                node_template: NodeTemplate
                for requirement_assignment in node_template.requirements:
                    requirement_assignment: RequirementAssignment
                    if requirement_assignment.relationship:
                        if type(requirement_assignment.relationship) == str and \
                                requirement_assignment.relationship == parent_relationship_template.name:
                            target_names.append(node_template.name)
                            break
                        elif type(requirement_assignment.relationship) == dict:
                            target_relationship = requirement_assignment.relationship.get('relationship')[1]
                            if target_relationship == parent_relationship_template:
                                target_names.append(node_template.name)
                                break
            value = value[1:]
            for target_name in target_names:
                find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment)
            return
        elif value[0] == 'TARGET':
            parent_relationship_template = find_parent_relationship_template(template_definition, property_assignment)
            for node_template in template_definition.node_templates:
                node_template: NodeTemplate
                for requirement_assignment in node_template.requirements:
                    requirement_assignment: RequirementAssignment
                    if requirement_assignment.relationship:
                        if type(requirement_assignment.relationship) == str and \
                                requirement_assignment.relationship == parent_relationship_template.name:
                            if type(requirement_assignment.node) == str:
                                target_names.append(requirement_assignment.node)
                            elif type(requirement_assignment.node) == dict:
                                target_names.append(requirement_assignment.node.get('node')[1].name)
                            break
                        elif type(requirement_assignment.relationship) == dict:
                            target_relationship = requirement_assignment.relationship.get('relationship')[1]
                            if target_relationship == parent_relationship_template:
                                if type(requirement_assignment.node) == str:
                                    target_names.append(requirement_assignment.node)
                                elif type(requirement_assignment.node) == dict:
                                    target_names.append(requirement_assignment.node.get('node')[1].name)
                                break
            value = value[1:]
            for target_name in target_names:
                find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment)
            return
        elif value[0] == 'HOST':
            parent_template = find_parent_template(template_definition, property_assignment)
            if parent_template is None:
                abort(400)
            for requirement_assignment in parent_template.requirements:
                requirement_assignment: RequirementAssignment
                if requirement_assignment.name == 'host':
                    if type(requirement_assignment.node) == str:
                        target_name = requirement_assignment.node
                    elif type(requirement_assignment.node) == dict:
                        target_vertex: NodeTemplate = requirement_assignment.node.get('node')[1]
                        target_name = target_vertex.name
                        value = value[1:]

        else:
            target_name = value[0]
            value = value[1:]
        for relationship_template in template_definition.relationship_templates:
            relationship_template: RelationshipTemplate
            if relationship_template.name == target_name:
                if find_in_property_list(property_assignment, relationship_template.properties, value[0]):
                    return
                if len(value) > 1:
                    for interface in relationship_template.interfaces:
                        interface: InterfaceDefinition
                        if interface.name == value[0]:
                            if find_in_property_list(property_assignment, interface.inputs, value[1]):
                                return

        if find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment):
            return
        if type(property_assignment.value) == dict and property_assignment.get_property is None:
            property_assignment.value = json.dumps(property_assignment.value)
    elif value.get('get_input'):
        target_name = value.get('get_input')
        target_name = target_name[0]
        for inputs in template_definition.inputs:
            inputs: ParameterDefinition
            if inputs.name == target_name:
                property_assignment.value = json.dumps(property_assignment.value)
                property_assignment.get_input = {'get_input': [property_assignment,
                                                               [inputs]]}
    else:
        abort(501)
