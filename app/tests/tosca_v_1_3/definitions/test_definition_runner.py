import unittest

from app.tests.tosca_v_1_3.definitions import TestArtifact, TestAttribute, TestCapability, TestConditionClause, \
    TestDescription, TestEventFilter, TestGroup, TestImperativeWorkflow, TestImport, TestInterface, TestNodeFilter, \
    TestNotification, TestNotificationImplementation, TestOperation, TestOperationImplementation, TestParameter, \
    TestPolicy, TestProperty, TestPropertyFilter, TestRepository, TestRequirement, TestSchema, TestServiceTemplate, TestTemplate, \
    TestTrigger, TestWorkflowPrecondition, TestWorkflowStep

definitionTestSuite = unittest.TestSuite()
definitionTestSuite.addTest(unittest.makeSuite(TestArtifact.TestArtifact))
definitionTestSuite.addTest(unittest.makeSuite(TestAttribute.TestAttribute))
definitionTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
definitionTestSuite.addTest(unittest.makeSuite(TestConditionClause.TestConditionClause))
definitionTestSuite.addTest(unittest.makeSuite(TestDescription.TestDescription))
definitionTestSuite.addTest(unittest.makeSuite(TestEventFilter.TestEventFilter))
definitionTestSuite.addTest(unittest.makeSuite(TestGroup.TestGroup))
definitionTestSuite.addTest(unittest.makeSuite(TestImperativeWorkflow.TestImperativeWorkflow))
definitionTestSuite.addTest(unittest.makeSuite(TestImport.TestImport))
definitionTestSuite.addTest(unittest.makeSuite(TestInterface.TestInterface))
definitionTestSuite.addTest(unittest.makeSuite(TestNodeFilter.TestNodeFilter))
definitionTestSuite.addTest(unittest.makeSuite(TestNotification.TestNotification))
definitionTestSuite.addTest(unittest.makeSuite(TestNotificationImplementation.TestNotificationImplementation))
definitionTestSuite.addTest(unittest.makeSuite(TestOperation.TestOperation))
definitionTestSuite.addTest(unittest.makeSuite(TestOperationImplementation.TestOperationImplementation))
definitionTestSuite.addTest(unittest.makeSuite(TestParameter.TestParameter))
definitionTestSuite.addTest(unittest.makeSuite(TestPolicy.TestPolicy))
definitionTestSuite.addTest(unittest.makeSuite(TestProperty.TestProperty))
definitionTestSuite.addTest(unittest.makeSuite(TestPropertyFilter.TestPropertyFilter))
definitionTestSuite.addTest(unittest.makeSuite(TestRepository.TestRepository))
definitionTestSuite.addTest(unittest.makeSuite(TestRequirement.TestRequirement))
definitionTestSuite.addTest(unittest.makeSuite(TestSchema.TestSchema))
definitionTestSuite.addTest(unittest.makeSuite(TestTemplate.TestTemplate))
definitionTestSuite.addTest(unittest.makeSuite(TestServiceTemplate.TestServiceTemplate))
definitionTestSuite.addTest(unittest.makeSuite(TestTrigger.TestTrigger))
definitionTestSuite.addTest(unittest.makeSuite(TestWorkflowPrecondition.TestWorkflowPrecondition))
definitionTestSuite.addTest(unittest.makeSuite(TestWorkflowStep.TestWorkflowStep))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(definitionTestSuite)
