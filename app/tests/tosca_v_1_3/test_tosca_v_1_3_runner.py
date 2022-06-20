import os
import subprocess

path = os.getcwd()
os.chdir(path + '/assignments')
from app.tests.tosca_v_1_3.assignments import test_assignment_runner
os.chdir(path + '/definitions')
from app.tests.tosca_v_1_3.definitions import test_definition_runner
os.chdir(path + '/others')
from app.tests.tosca_v_1_3.others import test_other_runner
os.chdir(path + '/types')
from app.tests.tosca_v_1_3.types import test_types_runner
