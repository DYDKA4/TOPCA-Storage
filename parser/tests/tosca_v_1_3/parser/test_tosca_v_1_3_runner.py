import os

from parser.tests.tosca_v_1_3.parser.assignments.test_assignment_runner import test_assignment_runner
from parser.tests.tosca_v_1_3.parser.definitions.test_definition_runner import test_definition_runner
from parser.tests.tosca_v_1_3.parser.others.test_other_runner import test_other_runner
from parser.tests.tosca_v_1_3.parser.types.test_types_runner import test_types_runner

path = os.getcwd()
os.chdir(path + '/types')
test_types_runner()
os.chdir(path + '/assignments')
test_assignment_runner()
os.chdir(path + '/definitions')
test_definition_runner()
os.chdir(path + '/others')
test_other_runner()
