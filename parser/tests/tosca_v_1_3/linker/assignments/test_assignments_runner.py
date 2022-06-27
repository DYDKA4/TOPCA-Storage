import unittest

from parser.tests.tosca_v_1_3.linker.assignments import test_link_requirement_assignments


def test_assignments_runner():
    assignmentTestSuite = unittest.TestSuite()
    assignmentTestSuite.addTest(unittest.makeSuite(test_link_requirement_assignments.TestRequirementAssignment))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(assignmentTestSuite)


