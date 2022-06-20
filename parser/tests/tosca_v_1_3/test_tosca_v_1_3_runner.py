import os
import subprocess


path = os.getcwd()
os.chdir(path + '/assignments')
from parser.tests.tosca_v_1_3.assignments import test_assignment_runner
os.chdir(path + '/definitions')
from parser.tests.tosca_v_1_3.definitions import test_definition_runner
os.chdir(path + '/others')
from parser.tests.tosca_v_1_3.others import test_other_runner
os.chdir(path + '/types')
from parser.tests.tosca_v_1_3.types import test_types_runner
