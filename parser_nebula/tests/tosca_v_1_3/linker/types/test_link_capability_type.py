import unittest

from parser_nebula.linker.tosca_v_1_3.types.CapabilityType import link_capability_type
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


class TestCapabilityType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.capability_types.append(CapabilityType('capability_type_parent'))
        self.capability = CapabilityType('capability_type')
        self.service_template.capability_types.append(self.capability)

    def test_link_derived_from(self):
        self.capability.derived_from = 'capability_type_parent'
        link_capability_type(self.service_template, self.capability)
        self.assertEqual(self.service_template.capability_types[0], self.capability.derived_from.get('derived_from')[1])

if __name__ == '__main__':
    unittest.main()
