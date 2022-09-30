import inspect
from parser.linker.LinkByName import link_by_type_name
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def link_requirement_assignments(service_template: ServiceTemplateDefinition, requirement: RequirementAssignment) -> None:
    template_definition: TemplateDefinition = service_template.topology_template
    if type(requirement.node) == str:
        link_by_type_name(template_definition.node_templates + service_template.node_types, requirement, 'node',)

    if type(requirement.relationship) == str:
        link_by_type_name(template_definition.relationship_templates + service_template.relationship_types,
                          requirement, 'relationship')

    if type(requirement.capability) == str:
        capabilities_list = []
        for node_type in service_template.node_types:
            capabilities_list += node_type.capabilities
        link_by_type_name(service_template.capability_types + capabilities_list, requirement, 'capability')
    if str in {type(requirement.node), type(requirement.relationship), type(requirement.capability)}:
        raise ParserException(400, inspect.stack()[0][3] +
                              ':  str in {type(requirement.node), type(requirement.relationship),'
                              ' type(requirement.capability)}')
