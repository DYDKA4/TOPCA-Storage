import unittest

from parser.linker.tosca_v_1_3.types.DataType import link_data_type
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.DataType import DataType


class TestDataType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.data_types.append(DataType('data_type_parent'))
        self.data = DataType('data_type')
        self.service_template.data_types.append(self.data)

    def test_link_derived_from(self):
        self.data.derived_from = 'data_type_parent'
        link_data_type(self.service_template, self.data)
        self.assertEqual(self.service_template.data_types[0], self.data.derived_from.get('derived_from')[1])

if __name__ == '__main__':
    unittest.main()
