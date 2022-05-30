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
#   # Optional declaration that exports the Topology Template
#   # as an implementation of a Node Type.
#   substitution_mappings:
#     <substitution_mappings>
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.ParameterDefinition import parameter_parser


class Template:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'TemplateDefinition'
        self.description = ""
        self.inputs = []

    def set_description(self, description: str):
        self.description = description

    def add_input(self, inputs):
        self.inputs.append(inputs)


def template_parser(data: dict) -> Template:
    template = Template()
    if data.get('topology_template'):
        data = data.get('topology_template')
    if data.get('description'):
        description = description_parser(data)
        template.set_description(description)
    if data.get('inputs'):
        for input_name, input_value in data.get('inputs').items():
            template.add_input(parameter_parser(input_name, input_value))

    return template
