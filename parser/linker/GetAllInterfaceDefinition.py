from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser.parser.tosca_v_1_3.types.NodeType import NodeType
from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def get_all_interface_definition(service_template: ServiceTemplateDefinition) -> list:
    interface_list = []
    for node_type in service_template.node_types:
        node_type: NodeType
        for requirement in node_type.requirements:
            requirement: RequirementDefinition
            interface_list += requirement.interfaces
        interface_list += node_type.interfaces
    for relationship_type in service_template.relationship_types:
        relationship_type: RelationshipType
        interface_list += relationship_type.interfaces
    if service_template.topology_template:
        topoly_template: TemplateDefinition = service_template.topology_template
        for relationship_template in topoly_template.relationship_templates:
            relationship_template: RelationshipTemplate
            interface_list += relationship_template.interfaces
        for node_template in topoly_template.node_templates:
            node_template: NodeTemplate
            interface_list += node_template.interfaces
            for requirement in node_template.requirements:
                requirement: RequirementAssignment
                interface_list += requirement.interfaces
