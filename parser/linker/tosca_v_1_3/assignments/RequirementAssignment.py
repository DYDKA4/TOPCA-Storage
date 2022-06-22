from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.linker.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_node(service_template: ServiceTemplateDefinition, requirement: RequirementAssignment) -> None:
    template_definition: TemplateDefinition = service_template.topology_template
    if type(requirement.node) == str:
        link_by_type_name(template_definition.node_templates, requirement, 'node',)
    if type(requirement.node) == str:
        link_by_type_name(service_template.node_types, requirement, 'node',)

    if type(requirement.relationship) == str:
        link_by_type_name(template_definition.relationship_templates, requirement, 'relationship')
    if type(requirement.relationship) == str:
        link_by_type_name(service_template.relationship_types, requirement, 'relationship')

    if type(requirement.capability) == str:
        link_by_type_name(service_template.capability_types, requirement, 'capability')
    if type(requirement.capability) == str:
        for node_type in service_template.node_types:
            link_by_type_name(node_type.capabilities, requirement, 'capability')
            if type(requirement.capability) != str:
                break
    if str in {type(requirement.node), type(requirement.relationship),type(requirement.capability)}:
        abort(400)
