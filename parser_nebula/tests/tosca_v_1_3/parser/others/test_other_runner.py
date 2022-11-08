import unittest

from parser_nebula.tests.tosca_v_1_3.parser.others import TestRelationshipTemplate, TestMetadata, TestDirectives, \
    TestNodeTemplate, TestConstraintClause


def test_other_runner():
    otherTestSuite = unittest.TestSuite()
    otherTestSuite.addTest(unittest.makeSuite(TestConstraintClause.TestConstraintClause))
    otherTestSuite.addTest(unittest.makeSuite(TestDirectives.TestDirectives))
    otherTestSuite.addTest(unittest.makeSuite(TestMetadata.TestMetadata))
    otherTestSuite.addTest(unittest.makeSuite(TestNodeTemplate.TestNodeTemplate))
    otherTestSuite.addTest(unittest.makeSuite(TestRelationshipTemplate.TestRelationshipTemplate))


    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(otherTestSuite)
