import unittest


from parser.tests.tosca_v_1_3.linker.other import test_link_node_template, test_link_relationship_template


def test_other_runner():
    assignmentTestSuite = unittest.TestSuite()
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_node_template.TestNodeTemplate))
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_relationship_template.TestRelationshipTemplate))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(assignmentTestSuite)
