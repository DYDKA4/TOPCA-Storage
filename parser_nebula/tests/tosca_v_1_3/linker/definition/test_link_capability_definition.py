import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.CapabilityDefinition import link_capability_definition
from parser_nebula.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


class TestCapabilityDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.capability_types.append(CapabilityType('capability_type'))
        self.capability = CapabilityDefinition('capability_definition')

    def test_link_artifact_type(self):
        self.capability.type = 'capability_type'
        link_capability_definition(self.service_template, self.capability)
        self.assertEqual(self.service_template.capability_types[0], self.capability.type.get('type')[1])

if __name__ == '__main__':
    unittest.main()
