import unittest

from parser.linker.tosca_v_1_3.definitions.AttributeDefinition import link_attribute_definition
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.DataType import DataType


class TestAttributeDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.data_types.append(DataType('data_type'))
        self.attribute = AttributeDefinition('attribute_definition')

    def test_link_artifact_type(self):
        self.attribute.type = 'data_type'
        link_attribute_definition(self.service_template, self.attribute)
        self.assertEqual(self.service_template.data_types[0], self.attribute.type.get('type')[1])

if __name__ == '__main__':
    unittest.main()
