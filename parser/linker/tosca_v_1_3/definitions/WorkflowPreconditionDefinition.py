# target: < target_name > Required
# target_relationship: < target_requirement_name >\
# condition:
# < list_of_condition_clause_definition >
import inspect

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_with_list
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions import WorkflowPreconditionDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def link_workflow_precondition_definition(service_template: ServiceTemplateDefinition,
                                          workflow: WorkflowPreconditionDefinition) -> None:
    array_to_find_target = []
    array_to_find_target_relationship = []
    topology_template: TemplateDefinition = service_template.topology_template
    if topology_template:
        array_to_find_target += topology_template.groups
        array_to_find_target_relationship += topology_template.relationship_templates
        array_to_find_target += topology_template.node_templates
    link_by_type_name(array_to_find_target, workflow, 'target')
    link_by_type_name(array_to_find_target_relationship, workflow, 'target_relationship')
    if str in {type(workflow.target), type(workflow.target_relationship)}:
        raise ParserException(400, inspect.stack()[0][3] + ': str in {type(workflow.target),'
                                                           ' type(workflow.target_relationship)}')
