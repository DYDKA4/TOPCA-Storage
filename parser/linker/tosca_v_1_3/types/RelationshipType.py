# <relationship_type_name>:
#   derived_from: <parent_relationship_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <relationship_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   interfaces:
#     <interface_definitions>
#   valid_target_types: [ <capability_type_names> ]
from werkzeug.exceptions import abort

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.linker.LinkerValidTypes import link_valid_target_types
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def link_relationship_type(service_template: ServiceTemplateDefinition,
                           relationship: RelationshipType) -> None:
    link_derived_from(service_template.relationship_types, relationship)
    link_valid_target_types(service_template.capability_types, relationship)
    if str in {type(relationship.derived_from)}:
        abort(400)
