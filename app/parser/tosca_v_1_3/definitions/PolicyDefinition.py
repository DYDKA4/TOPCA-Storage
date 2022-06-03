# <policy_name>:
#   type: # <policy_type_name> Required
#   description: <policy_description>
#   metadata:
#     <map of string>
#   properties:
#     <property_assignments>
#   targets: [<list_of_policy_targets>]
#   triggers:
#     <trigger_definitions>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.others.Metadata import Metadata
from app.parser.tosca_v_1_3.definitions.PropertyAssignment import PropertyAssignment
from app.parser.tosca_v_1_3.definitions.TriggerDefinition import TriggerDefinition, trigger_definition_parser


class PolicyDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.name = name
        self.vertex_type_system = 'PolicyDefinition'
        self.type = None
        self.description = None
        self.metadata = []
        self.properties = []
        self.targets = []
        self.triggers = []

    def set_type(self, group_type: str):
        self.type = group_type

    def set_description(self, description: str):
        self.description = description

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_property(self, properties: PropertyAssignment):
        self.properties.append(properties)

    def add_targets(self, target: str):
        self.targets.append(target)

    def add_trigger(self, trigger: TriggerDefinition):
        self.triggers.append(trigger)


def policy_definition_parser(name: str, data: dict) -> PolicyDefinition:
    policy = PolicyDefinition(name)
    if data.get('type'):
        policy.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        policy.set_description(description)
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            policy.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            policy.add_property(PropertyAssignment(property_name, property_value))
    if data.get('targets'):
        for target in data.get('targets'):
            policy.add_targets(target)
    if data.get('triggers'):
        for trigger_name, trigger_value in data.get('triggers'):
            policy.add_trigger(trigger_definition_parser(trigger_name,trigger_value))
    return policy
