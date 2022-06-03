# <policy_type_name>:
#   derived_from: <parent_policy_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <policy_description>
#   properties:
#     <property_definitions>
#   targets: [ <list_of_valid_target_types> ]
#   triggers:
#     <trigger_definitions>
from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.others.Metadata import Metadata
from app.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser
from app.parser.tosca_v_1_3.definitions.TriggerDefinition import TriggerDefinition, trigger_definition_parser


class PolicyType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'PolicyType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.properties = []
        self.targets = []
        self.triggers = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_target(self, target: str):
        self.targets.append(target)

    def add_trigger(self, trigger: TriggerDefinition):
        self.triggers.append(trigger)


def policy_type_parser(name: str, data: dict) -> PolicyType:
    policy = PolicyType(name)
    if data.get('derived_from'):
        policy.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        policy.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            policy.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            policy.set_description(description)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            policy.add_property(property_definition_parser(property_name, property_value))
    if data.get('targets'):
        for target in data.get('targets'):
            policy.add_target(target)
    if data.get('triggers'):
        for trigger_name, trigger_value in data.get('triggers'):
            policy.add_trigger(trigger_definition_parser(trigger_name, trigger_value))
    return policy
