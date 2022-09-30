# target: < target_name > Required
# target_relationship: < target_requirement_name >\
# condition:
# < list_of_condition_clause_definition >
import inspect

from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import ConditionClauseDefinition, \
    condition_clause_definition_parser


class WorkflowPreconditionDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'WorkflowPreconditionDefinition'
        self.target = None
        self.target_relationship = None
        self.conditions = []

    def set_target(self, target: str):
        self.target = target

    def set_target_relationship(self, target_relationship: str):
        self.target_relationship = target_relationship

    def add_condition(self, condition: ConditionClauseDefinition):
        self.conditions.append(condition)


def workflow_precondition_definition_parser(data: dict) -> WorkflowPreconditionDefinition:
    precondition = WorkflowPreconditionDefinition()
    if data.get('target'):
        precondition.set_target(data.get('target'))
    else:
        raise ParserException(400, inspect.stack()[0][3] + ': no_target')
    if data.get('target_relationship'):
        precondition.set_target_relationship(data.get('target_relationship'))
    if data.get('condition'):
        for condition_value in data.get('condition'):
            for key in condition_value.keys():
                precondition.add_condition(condition_clause_definition_parser(key, condition_value))
    return precondition
