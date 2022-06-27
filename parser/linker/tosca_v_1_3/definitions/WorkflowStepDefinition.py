# <step_name>:
#     target: <target_name> Required link
#     target_relationship: <target_requirement_name> link
#     operation_host: <operation_host_name>
#     filter:
#       - <list_of_condition_clause_definition>
#     activities: Required linker
#       - <list_of_activity_definition> #todo Remake if need it
#     on_success: linker
#       - <target_step_name>
#     on_failure: linker
#       - <target_step_name>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_with_list
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.definitions.WorkflowStepDefinition import WorkflowStepDefinition


def link_workflow_step_definition(service_template: ServiceTemplateDefinition,
                                  workflow: WorkflowStepDefinition) -> None:
    array_to_find_target = []
    array_to_find_target_relationship = []
    array_to_find_steps = []
    topology_template: TemplateDefinition = service_template.topology_template
    if topology_template:
        for workflow_imperative in topology_template.workflows:
            workflow_imperative: ImperativeWorkflowDefinition
            array_to_find_steps += workflow_imperative.steps

        array_to_find_target += topology_template.groups
        array_to_find_target_relationship += topology_template.relationship_templates
        array_to_find_target += topology_template.node_templates
    link_by_type_name(array_to_find_target, workflow, 'target')
    link_by_type_name(array_to_find_target_relationship, workflow, 'target_relationship')
    link_with_list(array_to_find_steps, workflow, 'on_success')
    link_with_list(array_to_find_steps, workflow, 'on_failure')
    if str in {type(workflow.target), type(workflow.target_relationship)}:
        abort(400)
