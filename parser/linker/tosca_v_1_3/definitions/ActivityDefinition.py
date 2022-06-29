from werkzeug.exceptions import abort

from parser.linker.GetAllArtifactDefinition import get_all_artifact_definition
from parser.linker.GetAllInterfaceDefinition import get_all_interface_definition
from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.ActivityDefinition import CallOperationActivityDefinition, \
    DelegateWorkflowActivityDefinition, InlineWorkflowActivityDefinition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def link_activity_definition(service_template: ServiceTemplateDefinition, activity):
    if activity.vertex_type_system == 'CallOperationActivityDefinition':
        activity: CallOperationActivityDefinition
        if activity.operation:
            operation: str = activity.operation
            operation_split = operation.split('.')
            operation = operation_split[-1]
            interface = operation_split[0]
            activity.interface_name = interface
            interface_definition_list = get_all_interface_definition(service_template)
            for interface_definition in interface_definition_list:
                interface_definition: InterfaceDefinition
                if interface_definition.name == interface:
                    for operation_definition in interface_definition.operations:
                        operation_definition: OperationDefinition
                        if operation_definition.name == operation:
                            activity.operation = {'operation': [activity, operation_definition]}
    if activity.vertex_type_system == 'DelegateWorkflowActivityDefinition':
        activity: DelegateWorkflowActivityDefinition
        topology_template: TemplateDefinition = service_template.topology_template
        link_by_type_name(topology_template.workflows, activity, 'workflow')
    if activity.vertex_type_system == 'InlineWorkflowActivityDefinition':
        activity: InlineWorkflowActivityDefinition
        topology_template: TemplateDefinition = service_template.topology_template
        link_by_type_name(topology_template.workflows, activity, 'workflow')
