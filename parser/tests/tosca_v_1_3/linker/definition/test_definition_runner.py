import unittest

from parser.tests.tosca_v_1_3.linker.definition import test_link_artifact_definition, \
    test_link_attribute_definition, test_link_capability_definition, test_link_event_filter_definition, \
    test_link_group_definition, test_link_interface_definition, test_link_notification_implementation_definition


def test_definition_runner():
    assignmentTestSuite = unittest.TestSuite()
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_artifact_definition.TestArtifactDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_attribute_definition.TestAttributeDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_capability_definition.TestCapabilityDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_event_filter_definition.TestEventFilterDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_group_definition.TestGroupDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_interface_definition.TestInterfaceDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_notification_implementation_definition.
                                                   TestNotificationImplementationDefinition))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(assignmentTestSuite)

test_definition_runner()