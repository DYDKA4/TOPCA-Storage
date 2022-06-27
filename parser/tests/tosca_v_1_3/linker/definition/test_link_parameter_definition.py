import unittest

from parser.linker.tosca_v_1_3.definitions.ParameterDefinition import link_parameter_definition
from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import ParameterDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.DataType import DataType


class TestParameterDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.data_types.append(DataType('data_type'))
        self.parameter = ParameterDefinition('parameter_definition')

    def test_link_artifact_type(self):
        self.parameter.type = 'data_type'
        link_parameter_definition(self.service_template, self.parameter)
        self.assertEqual(self.service_template.data_types[0], self.parameter.type.get('type')[1])

if __name__ == '__main__':
    unittest.main()
