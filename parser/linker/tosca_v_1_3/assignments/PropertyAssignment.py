import json
import warnings

from werkzeug.exceptions import abort

from parser.linker.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    link_notification_implementation_definition
from parser.linker.tosca_v_1_3.definitions.OperationDefinition import link_operation_definition
from parser.linker.tosca_v_1_3.definitions.OperationImplementationDefinition import \
    link_operation_implementation_definition
from parser.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment
from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import ParameterDefinition
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


def set_get_smt(property_assignment: PropertyAssignment, destination_property_assignment: object,
                get_type: str):
    if property_assignment.vertex_type_system != 'PropertyAssignment':
        abort(400)
    if type(getattr(property_assignment, get_type)) == dict:
        vertexes = getattr(property_assignment, get_type).get(get_type)
        new_destination: list = vertexes[1]
        new_destination.append(destination_property_assignment)
        setattr(property_assignment, get_type, {get_type: [property_assignment,
                                                           new_destination]})
    else:
        setattr(property_assignment, get_type, {get_type: [property_assignment,
                                                           [destination_property_assignment]]})
    if type(property_assignment.value) == dict:
        property_assignment.value = json.dumps(property_assignment.value)
    return


def find_in_property_list(property_assignment: PropertyAssignment, destination_property_assignment_list: list,
                          value: str):
    for destination_property_assignment in destination_property_assignment_list:
        destination_property_assignment: PropertyAssignment
        if destination_property_assignment.name == value:
            set_get_smt(property_assignment, destination_property_assignment, 'get_property')
            return True
    return False


def find_in_attribute_list(property_assignment: PropertyAssignment, attribute_list: list, value: str):
    for attribute_assignment in attribute_list:
        attribute_assignment: AttributeAssignment
        if attribute_assignment.name == value:
            set_get_smt(property_assignment, attribute_assignment, 'get_attribute')
            return True
    return False


def find_in_artifact_list(property_assignment, artifact_list, value: str):
    for artifact_definition in artifact_list:
        artifact_definition: ArtifactDefinition
        if artifact_definition.name == value:
            set_get_smt(property_assignment, artifact_definition, 'get_artifact')
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
        for interface_definition in node_template.interfaces:
            interface_definition: InterfaceDefinition
            for inputs_property_assignment in interface_definition.inputs:
                inputs_property_assignment: PropertyAssignment
                if inputs_property_assignment.vertex_type_system != "PropertyAssignment":
                    abort(400)
                if inputs_property_assignment == property_assignment:
                    return node_template
        for requirement_assignment in node_template.requirements:
            requirement_assignment: RequirementAssignment
            for requirement_property_assignment in requirement_assignment.properties:
                requirement_property_assignment: PropertyAssignment
                if requirement_property_assignment == property_assignment:
                    return node_template
            for interface_definition in requirement_assignment.interfaces:
                interface_definition: InterfaceDefinition
                for inputs_property_assignment in interface_definition.inputs:
                    if inputs_property_assignment.vertex_type_system != "PropertyAssignment":
                        abort(400)
                    if inputs_property_assignment == property_assignment:
                        return node_template
    return None


def find_parent_relationship_template(template_definition: TemplateDefinition, property_assignment):
    for relationship_template in template_definition.relationship_templates:
        relationship_template: RelationshipTemplate
        for property_assignment_copy in relationship_template.properties:
            property_assignment_copy: PropertyAssignment
            if property_assignment_copy == property_assignment:
                return relationship_template
        for interface_definition in relationship_template.interfaces:
            interface_definition: InterfaceDefinition
            for inputs_property_assignment in interface_definition.inputs:
                inputs_property_assignment: PropertyAssignment
                if inputs_property_assignment.vertex_type_system != "PropertyAssignment":
                    abort(400)
                if inputs_property_assignment == property_assignment:
                    return relationship_template
    return None


def find_parent_policy_definition(template_definition: TemplateDefinition, property_assignment):
    for policy_definition in template_definition.policies:
        policy_definition: PolicyDefinition
        for property_assignment_copy in policy_definition.properties:
            property_assignment_copy: PropertyAssignment
            if property_assignment_copy == property_assignment:
                return policy_definition
    return None


def find_parent_group_definition(template_definition: TemplateDefinition, property_assignment):
    for group_definition in template_definition.groups:
        group_definition: GroupDefinition
        for property_assignment_copy in group_definition.properties:
            property_assignment_copy: PropertyAssignment
            if property_assignment_copy == property_assignment:
                return group_definition
    return None


def find_in_interface_artifact(value, property_assignment, interface_list: list,
                               service_template: ServiceTemplateDefinition):
    artifact_list = []
    for interface_definition in interface_list:
        interface_definition: InterfaceDefinition
        for operation_definition in interface_definition.operations:
            operation_definition: OperationDefinition
            if operation_definition.implementation is None:
                break
            if type(operation_definition.implementation) == str:
                link_operation_definition(service_template, operation_definition)
            if type(operation_definition.implementation) == dict:
                artifact_list.append(operation_definition.implementation.get('implementation')[1])
            else:
                operation_implementation: OperationImplementationDefinition = \
                    operation_definition.implementation
                if type(operation_implementation.primary) == str:
                    link_operation_implementation_definition(service_template, operation_implementation)
                if type(operation_implementation) == dict:
                    artifact_list.append(operation_implementation.primary.get('primary')[1])
                else:
                    artifact_list.append(operation_implementation.primary)
        for notification_definition in interface_definition.notifications:
            notification_definition: NotificationDefinition
            if notification_definition.implementation is not None:
                notification_implementation: NotificationImplementationDefinition = \
                    notification_definition.implementation
                if type(notification_implementation.primary) == str:
                    link_notification_implementation_definition(service_template,
                                                                notification_implementation)
                artifact_list.append(notification_implementation.primary.get('primary')[1])
    if find_in_artifact_list(property_assignment, artifact_list, value[0]):
        return True
    return False


def find_in_node_template_list(node_templates: list, target_name, value, property_assignment, attribute_flag,
                               artifact_flag, service_template: ServiceTemplateDefinition):
    for node_template in node_templates:
        node_template: NodeTemplate
        if node_template.name == target_name:
            if attribute_flag:
                if find_in_attribute_list(property_assignment, node_template.attributes, value[0]):
                    return True
                if len(value) > 1:
                    for capability_assignment in node_template.capabilities:
                        capability_assignment: CapabilityAssignment
                        if capability_assignment.name == value[0]:
                            if find_in_attribute_list(property_assignment, capability_assignment.attributes, value[1]):
                                return True
            elif artifact_flag:
                if find_in_artifact_list(property_assignment, node_template.artifacts, value[0]):
                    return True
                elif find_in_interface_artifact(value, property_assignment, node_template.interfaces, service_template):
                    return True
            else:
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


def find_in_group_definition_list(group_definitions: list, target_name, value, property_assignment: PropertyAssignment,
                                  attribute_flag):
    for group_definition in group_definitions:
        group_definition: GroupDefinition
        if group_definition.name == target_name:
            if attribute_flag:
                if find_in_attribute_list(property_assignment, group_definition.attributes, value[0]):
                    return True
            else:
                if find_in_property_list(property_assignment, group_definition.properties, value[0]):
                    return True
    return False


def find_in_policy_definition_list(policy_definitions: list, target_name, value,
                                   property_assignment: PropertyAssignment, attribute_flag: bool):
    for policy_definition in policy_definitions:
        policy_definition: PolicyDefinition
        if policy_definition.name == target_name:
            if attribute_flag:
                return False
            else:
                if find_in_property_list(property_assignment, policy_definition.properties, value[0]):
                    return True
    return False


def find_in_relationship_template_list(relationship_templates: list, target_name, value,
                                       property_assignment: PropertyAssignment, attribute_flag, artifact_flag,
                                       service_template: ServiceTemplateDefinition):
    for relationship_template in relationship_templates:
        relationship_template: RelationshipTemplate
        if relationship_template.name == target_name:
            if attribute_flag:
                if find_in_attribute_list(property_assignment, relationship_template.attributes, value[0]):
                    return
            elif artifact_flag:
                if find_in_interface_artifact(value, property_assignment, relationship_template.interfaces,
                                              service_template):
                    return True
            else:
                if find_in_property_list(property_assignment, relationship_template.properties, value[0]):
                    return
                if len(value) > 1:
                    for interface in relationship_template.interfaces:
                        interface: InterfaceDefinition
                        if interface.name == value[0]:
                            if find_in_property_list(property_assignment, interface.inputs, value[1]):
                                return


def link_property_assignment(service_template: ServiceTemplateDefinition,
                             property_assignment: PropertyAssignment) -> None:
    template_definition: TemplateDefinition = service_template.topology_template
    if type(property_assignment.value) == dict:
        value = property_assignment.value
    else:
        return
    if value.get('get_property') or value.get('get_attribute') or value.get('get_artifact'):
        if value.get('get_property'):
            value = value.get('get_property')
            attribute_flag = False
            artifact_flag = False
        elif value.get('get_artifact'):
            value = value.get('get_artifact')
            attribute_flag = False
            artifact_flag = True
        else:
            value = value.get('get_attribute')
            attribute_flag = True
            artifact_flag = False
        target_name = ''
        target_names = []
        if value[0] == 'SELF':
            if find_parent_template(template_definition, property_assignment):
                parent_template: NodeTemplate = find_parent_template(template_definition, property_assignment)
                value = value[1:]
                target_name = parent_template.name
            elif find_parent_relationship_template(template_definition, property_assignment):
                parent_template: RelationshipTemplate = find_parent_relationship_template(template_definition,
                                                                                          property_assignment)
                value = value[1:]
                target_name = parent_template.name
            # elif find_parent_group_definition(template_definition, property_assignment):
            #     parent_template: GroupDefinition = find_parent_group_definition(template_definition,
            #                                                                     property_assignment)
            #     value = value[1:]
            #     target_name = parent_template.name
            # elif find_parent_policy_definition(template_definition, property_assignment):
            #     parent_template: PolicyDefinition = find_parent_policy_definition(template_definition,
            #                                                                       property_assignment)
            #     value = value[1:]
            #     target_name = parent_template.name
            else:
                abort(400)
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
                find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment,
                                           attribute_flag, artifact_flag, service_template)
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
                find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment,
                                           attribute_flag, artifact_flag, service_template)
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
        if find_in_relationship_template_list(template_definition.relationship_templates, target_name, value,
                                              property_assignment, attribute_flag, artifact_flag, service_template):
            return
        elif find_in_node_template_list(template_definition.node_templates, target_name, value, property_assignment,
                                        attribute_flag, artifact_flag, service_template):
            return
        elif not artifact_flag and find_in_policy_definition_list(template_definition.policies, target_name, value,
                                                                  property_assignment, attribute_flag):
            return
        elif not artifact_flag and find_in_group_definition_list(template_definition.groups, target_name, value,
                                                                 property_assignment, attribute_flag):
            return
        elif type(property_assignment.value) == dict and property_assignment.get_property is None:
            property_assignment.value = json.dumps(property_assignment.value)
    elif value.get('get_input'):
        target_name = value.get('get_input')
        if type(target_name) == str:
            abort(400)
        target_name = target_name[0]
        for inputs in template_definition.inputs:
            inputs: ParameterDefinition
            if inputs.name == target_name:
                property_assignment.value = json.dumps(property_assignment.value)
                property_assignment.get_input = {'get_input': [property_assignment,
                                                               [inputs]]}
    else:
        warnings.warn(f'Unsuccessful try to link {value}')
        abort(501)
