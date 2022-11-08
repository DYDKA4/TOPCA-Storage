import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.SchemaDefinition import link_schema_definition
from parser_nebula.parser.tosca_v_1_3.definitions.SchemaDefinition import SchemaDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.DataType import DataType


class TestSchemaDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.data_types.append(DataType('data_type_root'))
        self.service_template.data_types.append(DataType('data_key'))
        self.service_template.data_types.append(DataType('data_entry'))
        self.schema = SchemaDefinition()

    def test_link_data_type(self):
        self.schema.type = 'data_type_root'
        link_schema_definition(self.service_template, self.schema)
        self.assertEqual(self.service_template.data_types[0], self.schema.type.get('type')[1])

    def test_link_entry_data_type(self):
        self.schema.key_schema = SchemaDefinition()
        self.schema.key_schema.type = 'data_key'
        link_schema_definition(self.service_template, self.schema)
        self.assertEqual(self.service_template.data_types[1],
                         self.schema.key_schema.type.get('type')[1])

    def test_link_key_data_type(self):
        self.schema.entry_schema = SchemaDefinition()
        self.schema.entry_schema.type = 'data_entry'
        link_schema_definition(self.service_template, self.schema)
        self.assertEqual(self.service_template.data_types[2],
                         self.schema.entry_schema.type.get('type')[1])


if __name__ == '__main__':
    unittest.main()
