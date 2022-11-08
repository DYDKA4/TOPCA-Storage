import unittest

from parser_nebula.tests.tosca_v_1_3.linker.types import test_link_artifact_type, test_link_capability_type, \
    test_link_data_type, test_link_group_type, test_link_interface_type, test_link_node_type, test_link_policy_type, \
    test_link_relationship_type


def test_types_runner():
    assignmentTestSuite = unittest.TestSuite()
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_artifact_type.TestArtifactType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_capability_type.TestCapabilityType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_data_type.TestDataType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_group_type.TestGroupType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_interface_type.TestInterfaceType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_node_type.TestNodeType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_policy_type.TestPolicyType))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_relationship_type.TestRelationshipType))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(assignmentTestSuite)


