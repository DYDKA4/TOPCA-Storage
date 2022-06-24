from parser.linker.tosca_v_1_3.definitions.ArtifactDefinition import link_artifact_definition
from parser.linker.tosca_v_1_3.definitions.AttributeDefinition import link_attribute_definition
from parser.linker.tosca_v_1_3.definitions.CapabilityDefinition import link_capability_definition
from parser.linker.tosca_v_1_3.definitions.EventFilterDefinition import link_event_filter_definition
from parser.linker.tosca_v_1_3.definitions.GroupDefinition import link_group_definition
from parser.linker.tosca_v_1_3.definitions.InterfaceDefinition import link_interface_definition
from parser.linker.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    link_notification_implementation_definition
from parser.linker.tosca_v_1_3.definitions.OperationDefinition import link_operation_definition
from parser.linker.tosca_v_1_3.definitions.OperationImplementationDefinition import \
    link_operation_implementation_definition
from parser.linker.tosca_v_1_3.definitions.ParameterDefinition import link_parameter_definition
from parser.linker.tosca_v_1_3.definitions.PolicyDefinition import link_policy_definition
from parser.linker.tosca_v_1_3.definitions.PropertyDefinition import link_property_definition
from parser.linker.tosca_v_1_3.definitions.RequirementDefinition import link_requirement_definition
from parser.linker.tosca_v_1_3.definitions.SchemaDefinition import link_schema_definition
from parser.linker.tosca_v_1_3.definitions.WorkflowPreconditionDefinition import link_workflow_precondition_definition
from parser.linker.tosca_v_1_3.definitions.WorkflowStepDefinition import link_workflow_step_definition
from parser.linker.tosca_v_1_3.others.NodeTemplate import link_node_template
from parser.linker.tosca_v_1_3.others.RelationshipTemplate import link_relationship_template
from parser.linker.tosca_v_1_3.types.ArtifactType import link_artifact_type
from parser.linker.tosca_v_1_3.types.CapabilityType import link_capability_type
from parser.linker.tosca_v_1_3.types.DataType import link_data_type
from parser.linker.tosca_v_1_3.types.GroupType import link_group_type
from parser.linker.tosca_v_1_3.types.InterfaceType import link_interface_type
from parser.linker.tosca_v_1_3.types.NodeType import link_node_type
from parser.linker.tosca_v_1_3.types.PolicyTypes import link_policy_type
from parser.linker.tosca_v_1_3.types.RelationshipType import link_relationship_type
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition
from parser.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.NodeFilterDefinition import NodeFilterDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition
from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TriggerDefinition import TriggerDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType
from parser.parser.tosca_v_1_3.types.CapabilityType import CapabilityType
from parser.parser.tosca_v_1_3.types.DataType import DataType
from parser.parser.tosca_v_1_3.types.GroupType import GroupType
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType
from parser.parser.tosca_v_1_3.types.NodeType import NodeType
from parser.parser.tosca_v_1_3.types.PolicyTypes import PolicyType
from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def sub_interface_definition_parser(interfaces_list, service_template: ServiceTemplateDefinition):
    for interface_definition in interfaces_list:
        interface_definition: InterfaceDefinition
        link_interface_definition(service_template, interface_definition)
        for notification_definition in interface_definition.notifications:
            notification_definition: NotificationDefinition
            if notification_definition.implementation and type(notification_definition.implementation) != dict:
                link_notification_implementation_definition(service_template, notification_definition.implementation)
        for operation_definition in interface_definition.operations:
            operation_definition: OperationDefinition
            link_operation_definition(service_template, operation_definition)
            if operation_definition.implementation and type(operation_definition.implementation) != dict:
                link_operation_implementation_definition(service_template, operation_definition.implementation)



def sub_attribute_definition_parser(service_template: ServiceTemplateDefinition, attribute_list: list):
    for attribute_definition in attribute_list:
        attribute_definition: AttributeDefinition
        link_attribute_definition(service_template, attribute_definition)
        if attribute_definition.key_schema:
            link_schema_definition(service_template, attribute_definition.key_schema)
        if attribute_definition.entry_schema:
            link_schema_definition(service_template, attribute_definition.entry_schema)



def main_linker(service_template: ServiceTemplateDefinition):
    for artifact_type in service_template.artifact_types:
        artifact_type: ArtifactType
        for property_definition in artifact_type.properties:
            link_property_definition(service_template, property_definition)
        link_artifact_type(service_template, artifact_type)
    for data_type in service_template.data_types:
        data_type: DataType
        for property_definition in data_type.properties:
            link_property_definition(service_template, property_definition)
        link_data_type(service_template, data_type)
    for capability_type in service_template.capability_types:
        capability_type: CapabilityType
        for property_definition in capability_type.properties:
            link_property_definition(service_template, property_definition)
        sub_attribute_definition_parser(service_template, capability_type.attributes)
        link_capability_type(service_template, capability_type)
    for interface_type in service_template.interface_types:
        interface_type: InterfaceType
        for property_definition in interface_type.inputs:
            link_property_definition(service_template, property_definition)
        for notification_definition in interface_type.notifications:
            notification_definition: NotificationDefinition
            if notification_definition.implementation and type(notification_definition.implementation) != dict:
                link_notification_implementation_definition(service_template, notification_definition.implementation)
        for operation_definition in interface_type.operations:
            operation_definition: OperationDefinition
            link_operation_definition(service_template, operation_definition)
            if operation_definition.implementation and type(operation_definition.implementation) != dict:
                link_operation_implementation_definition(service_template, operation_definition.implementation)
        link_interface_type(service_template, interface_type)
    for relationship_type in service_template.relationship_types:
        relationship_type: RelationshipType
        sub_attribute_definition_parser(service_template, relationship_type.attributes)
        sub_interface_definition_parser(relationship_type.interfaces, service_template)
        link_relationship_type(service_template, relationship_type)
    for node_type in service_template.node_types:
        node_type: NodeType
        for property_definition in node_type.properties:
            link_property_definition(service_template, property_definition)
        sub_attribute_definition_parser(service_template, node_type.attributes)
        for requirement_definition in node_type.requirements:
            requirement_definition: RequirementDefinition
            link_requirement_definition(service_template, requirement_definition)
            sub_interface_definition_parser(requirement_definition.interfaces, service_template)
        for capabilities_definition in node_type.capabilities:
            capabilities_definition: CapabilityDefinition
            link_capability_definition(service_template, capabilities_definition)
            for property_definition in capabilities_definition.properties:
                link_property_definition(service_template, property_definition)
            sub_attribute_definition_parser(service_template, capabilities_definition.attributes)
        sub_interface_definition_parser(node_type.interfaces, service_template)
        for artifact_definition in node_type.artifacts:
            link_artifact_definition(service_template, artifact_definition)
        link_node_type(service_template, node_type)
    for group_type in service_template.group_types:
        group_type: GroupType
        sub_attribute_definition_parser(service_template, group_type.attributes)
        for property_definition in group_type.properties:
            link_property_definition(service_template, property_definition)
        link_group_type(service_template, group_type)
    for policy_type in service_template.policy_types:
        policy_type: PolicyType
        for property_definition in policy_type.properties:
            link_property_definition(service_template, property_definition)
        for trigger_definition in policy_type.triggers:
            trigger_definition: TriggerDefinition
            # link_trigger_definition
            if trigger_definition.event_filter:
                link_event_filter_definition(service_template, trigger_definition.event_filter)
        link_policy_type(service_template, policy_type)
    if service_template.topology_template:
        topology_template: TemplateDefinition = service_template.topology_template
        for inputs in topology_template.inputs:
            link_parameter_definition(service_template, inputs)
        for outputs in topology_template.outputs:
            link_parameter_definition(service_template, outputs)
        for node_template in topology_template.node_templates:
            node_template: NodeTemplate
            for requirement_assignment in node_template.requirements:
                requirement_assignment: RequirementAssignment
                sub_interface_definition_parser(requirement_assignment.interfaces, service_template)
                # if requirement_assignment.node_filter:
                #     node_filter: NodeFilterDefinition = requirement_assignment.node_filter
            for artifact_definition in node_template.artifacts:
                link_artifact_definition(service_template, artifact_definition)
            link_node_template(service_template, node_template)
        for relationship_template in topology_template.relationship_templates:
            relationship_template: RelationshipTemplate
            sub_interface_definition_parser(relationship_template.interfaces, service_template)
            link_relationship_template(service_template, relationship_template)
        for group_definition in topology_template.groups:
            group_definition: GroupDefinition
            link_group_definition(service_template, group_definition)
        for policy_definition in topology_template.policies:
            policy_definition: PolicyDefinition
            link_policy_definition(service_template, policy_definition)
            for trigger_definition in policy_definition.triggers:
                trigger_definition: TriggerDefinition
                # link_trigger_definition
                if trigger_definition.event_filter:
                    link_event_filter_definition(service_template, trigger_definition.event_filter)
        for imperative_workflow_definition in topology_template.workflows:
            imperative_workflow_definition: ImperativeWorkflowDefinition
            for property_definition in imperative_workflow_definition.inputs:
                link_property_definition(service_template, property_definition)
            for workflow_precondition_definition in imperative_workflow_definition.preconditions:
                link_workflow_precondition_definition(service_template, workflow_precondition_definition)
            for workflow_step_definition in imperative_workflow_definition.steps:
                link_workflow_step_definition(service_template, workflow_step_definition)
            for operation_implementation_definition in imperative_workflow_definition.implementation:
                link_operation_implementation_definition(service_template, operation_implementation_definition)
