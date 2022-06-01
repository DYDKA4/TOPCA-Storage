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
#     <substitution_mappings>
# todo relationship_templates groups policies workflows substitution_mappings
from app.data_classes import RelationshipTemplate
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.GroupDefinition import GroupDefinition, group_definition_parser
from app.parser.tosca_v_1_3.NodeTemplate import NodeTemplate, node_template_parser
from app.parser.tosca_v_1_3.ParameterDefinition import parameter_parser, Parameter
from app.parser.tosca_v_1_3.RelationshipTemplate import relationship_template_parser


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

    def set_description(self, description: str):
        self.description = description

    def add_input(self, inputs: Parameter):
        self.inputs.append(inputs)

    def add_output(self, outputs: Parameter):
        self.outputs.append(outputs)

    def add_node_templates(self, node_template: NodeTemplate):
        self.node_templates.append(node_template)

    def add_relationship_template(self, relationship_template: RelationshipTemplate):
        self.relationship_templates.append(relationship_template)

    def add_group(self, group: GroupDefinition):
        self.groups.append(group)


def template_parser(data: dict) -> TemplateDefinition:
    template = TemplateDefinition()
    if data.get('topology_template'):
        data = data.get('topology_template')
    if data.get('description'):
        description = description_parser(data)
        template.set_description(description)
    if data.get('inputs'):
        for input_name, input_value in data.get('inputs').items():
            template.add_input(parameter_parser(input_name, input_value))
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
        
    # policies

    if data.get('outputs'):
        for output_name, output_value in data.get('outputs').items():
            template.add_output(parameter_parser(output_name, output_value))
    # substitution_mappings
    # workflows
    return template
