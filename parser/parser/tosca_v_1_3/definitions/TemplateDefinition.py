# topology_template:
#   description: <template_description>
#   inputs: <input_parameters>
#   outputs: <output_parameters>
#   node_templates: <node_templates>
#   relationship_templates: <relationship_templates>
#   groups: <group_definitions>
#   policies:
#     - <policy_definition_list>
#   workflows: <workflows>
#   # Optional declaration that exports the Topology TemplateDefinition
#   # as an implementation of a Node Type.
#   substitution_mappings:
#     <substitution_mappings> #todo What is it?
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition, group_definition_parser
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition, \
    imperative_workflow_definition_parser
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate, node_template_parser
from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import parameter_definition_parser, ParameterDefinition
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition, policy_definition_parser
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import relationship_template_parser, RelationshipTemplate


class TemplateDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'TemplateDefinition'
        self.description = None
        self.inputs = []
        self.outputs = []
        self.node_templates = []
        self.relationship_templates = []
        self.groups = []
        self.policies = []
        self.workflows = []
        self.substitution_mappings = None

    def set_description(self, description: str):
        self.description = description

    def add_input(self, inputs: ParameterDefinition):
        self.inputs.append(inputs)

    def add_output(self, outputs: ParameterDefinition):
        self.outputs.append(outputs)

    def add_node_templates(self, node_template: NodeTemplate):
        self.node_templates.append(node_template)

    def add_relationship_template(self, relationship_template: RelationshipTemplate):
        self.relationship_templates.append(relationship_template)

    def add_group(self, group: GroupDefinition):
        self.groups.append(group)

    def add_policy(self, policy: PolicyDefinition):
        self.policies.append(policy)

    def add_workflow(self, workflow: ImperativeWorkflowDefinition):
        self.workflows.append(workflow)

    def set_substitution_mappings(self, substitution_mappings: str):
        self.substitution_mappings = substitution_mappings


def template_definition_parser(data: dict) -> TemplateDefinition:
    template = TemplateDefinition()
    if data.get('topology_template'):
        data = data.get('topology_template')
    else:
        return template
    if data.get('description'):
        description = description_parser(data)
        template.set_description(description)
    if data.get('inputs'):
        for input_name, input_value in data.get('inputs').items():
            template.add_input(parameter_definition_parser(input_name, input_value))
    if data.get('node_templates'):
        for node_template_name, node_template_value in data.get('node_templates').items():
            template.add_node_templates(node_template_parser(node_template_name, node_template_value))
    if data.get('relationship_templates'):
        for relationship_name, relationship_value in data.get('relationship_templates').items():
            template.add_relationship_template(relationship_template_parser(relationship_name,relationship_value))
    if data.get('groups'):
        for group_name, group_value in data.get('groups').items():
            template.add_group(group_definition_parser(group_name, group_value))
    if data.get('policies'):
        for policy in data.get('policies'):
            for policy_name, policy_value in policy.items():
                template.add_policy(policy_definition_parser(policy_name, policy_value))
    if data.get('outputs'):
        for output_name, output_value in data.get('outputs').items():
            template.add_output(parameter_definition_parser(output_name, output_value))
    if data.get('workflows'):
        for workflow_name, workflow_value in data.get('workflows').items():
            template.add_workflow(imperative_workflow_definition_parser(workflow_name, workflow_value))
    if data.get('substitution_mappings'):
        template.set_substitution_mappings(str(data.get('substitution_mappings')))
    return template
