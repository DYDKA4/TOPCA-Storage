# <data_type_name>:
#   derived_from: <existing_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <datatype_description>
#   constraints:
#     - <type_constraints>
#   properties:
#     <property_definitions>
#   key_schema : <key_schema_definition>
#   entry_schema: <entry_schema_definition>
import inspect

from parser_nebula.linker.LinkDerivedFrom import link_derived_from
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.DataType import DataType


def link_data_type(service_template: ServiceTemplateDefinition,
                         data: DataType) -> None:
    link_derived_from(service_template.data_types, data)
    if str in {type(data.derived_from)}:
        raise ParserException(400, inspect.stack()[0][3] + ': str in {type(data.derived_from)}')
