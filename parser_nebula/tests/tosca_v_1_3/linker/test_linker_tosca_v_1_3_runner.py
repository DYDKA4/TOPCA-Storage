import os

from parser_nebula.tests.tosca_v_1_3.linker.assignments.test_assignments_runner import test_assignments_runner
from parser_nebula.tests.tosca_v_1_3.linker.definition.test_definition_runner import test_definition_runner
from parser_nebula.tests.tosca_v_1_3.linker.other.test_other_runner import test_other_runner
from parser_nebula.tests.tosca_v_1_3.linker.types.test_types_runner import test_types_runner

path = os.getcwd()
os.chdir(path + '/types')
test_types_runner()
os.chdir(path + '/assignments')
test_assignments_runner()
os.chdir(path + '/definition')
test_definition_runner()
os.chdir(path + '/other')
test_other_runner()
