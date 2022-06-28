# <step_name>:
#     target: <target_name> Required
#     target_relationship: <target_requirement_name>
#     operation_host: <operation_host_name>
#     filter:
#       - <list_of_condition_clause_definition>
#     activities: Required
#       - <list_of_activity_definition> #todo Remake if need it
#     on_success:
#       - <target_step_name>
#     on_failure:
#       - <target_step_name>
from werkzeug.exceptions import abort

from parser.parser.tosca_v_1_3.definitions.ActivityDefinition import activity_definition_parser
from parser.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import condition_clause_definition_parser, \
    ConditionClauseDefinition


class WorkflowStepDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'WorkflowStepDefinition'
        self.name = name
        self.target = None
        self.target_relationship = None
        self.operation_host = None
        self.filter = []
        self.activities = []
        self.on_success = []
        self.on_failure = []

    def set_target(self, target: str):
        self.target = target

    def set_target_relationship(self, target_relationship: str):
        self.target_relationship = target_relationship

    def set_operation_host(self, operation_host: str):
        self.operation_host = operation_host

    def add_filter(self, filters: ConditionClauseDefinition):
        self.filter.append(filters)

    def add_activities(self, activities: object):
        self.activities.append(activities)

    def add_on_success(self, on_success: str):
        self.on_success.append(on_success)

    def add_on_failure(self, on_failure: str):
        self.on_failure.append(on_failure)


def workflow_step_definition_parser(name: str, data: dict) -> WorkflowStepDefinition:
    step = WorkflowStepDefinition(name)
    if data.get('target'):
        step.set_target(data.get('target'))
    else:
        abort(400)
    if data.get('target_relationship'):
        step.set_target_relationship(data.get('target_relationship'))
    if data.get('operation_host'):
        step.set_operation_host(data.get('operation_host'))
    if data.get('filter'):
        for filters in data.get('filter'):
            for key in filters.keys():
                step.add_filter(condition_clause_definition_parser(key, filters))
    if data.get('activities'):
        for activities in data.get('activities'):
            step.add_activities(activity_definition_parser(activities))
    else:
        abort(400)
    if data.get('on_success'):
        for on_success in data.get('on_success'):
            step.add_on_success(on_success)
    if data.get('on_failure'):
        for on_failure in data.get('on_failure'):
            step.add_on_failure(on_failure)
    return step
