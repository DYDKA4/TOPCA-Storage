import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.PropertyDefinition import link_property_definition
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.DataType import DataType


class TestPropertyDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.data_types.append(DataType('data_type'))
        self.property = PropertyDefinition('parameter_definition')

    def test_link_property_type(self):
        self.property.type = 'data_type'
        link_property_definition(self.service_template, self.property)
        self.assertEqual(self.service_template.data_types[0], self.property.type.get('type')[1])

if __name__ == '__main__':
    unittest.main()
