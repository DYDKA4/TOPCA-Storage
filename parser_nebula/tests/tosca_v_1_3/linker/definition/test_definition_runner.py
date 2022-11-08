import unittest

from parser_nebula.tests.tosca_v_1_3.linker.definition import test_link_artifact_definition, \
    test_link_attribute_definition, test_link_capability_definition, test_link_event_filter_definition, \
    test_link_group_definition, test_link_interface_definition, test_link_notification_implementation_definition, \
    test_link_operation_definition, test_link_operation_implementation_definition, test_link_parameter_definition, \
    test_link_policy_definition, test_link_property_definition, test_link_requirement_definition, \
    test_link_schema_definition, test_link_workflow_precondition_definition, test_link_workflow_step_definition


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
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_operation_definition.TestOperationDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_operation_implementation_definition.
                                                   TestOperationImplementationDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_parameter_definition.TestParameterDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_policy_definition.TestPolicyDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_property_definition.TestPropertyDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_requirement_definition.TestRequirementDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_schema_definition.TestSchemaDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_workflow_precondition_definition.
                                                   TestWorkflowPreconditionDefinition))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_workflow_step_definition.TestWorkflowStepDefinition))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(assignmentTestSuite)


