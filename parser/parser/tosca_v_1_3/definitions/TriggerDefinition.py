# Short notation
# <trigger_name>:
#   description: <trigger_description>
#   event: <event _name> Required
#   schedule: <time_interval_for_trigger>
#   target_filter:
#     <event_filter_definition>
#   condition:
#     <condition_clause_definition>
#   action:
#     - <list_of_activity_definition> #todo Remake if need it

# Extended notation:
# <trigger_name>:
#   description: <trigger_description>
#   event: <event _name>
#   schedule: <time_interval_for_trigger>
#   target_filter:
#     <event_filter_definition>
#   condition:
#     constraint: <condition_clause_definition>
#     period: <scalar-unit.time> # e.g., 60 sec
#     evaluations: <integer> # e.g., 1
#     method: <string> # e.g., average
#   action:
#     - <list_of_activity_definition> #todo Remake if need it
from werkzeug.exceptions import abort

from parser.parser.tosca_v_1_3.definitions.ActivityDefinition import activity_definition_parser
from parser.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import ConditionClauseDefinition, \
    condition_clause_definition_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition


class TriggerDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.name = name
        self.vertex_type_system = 'TriggerDefinition'
        self.description = None
        self.event = None
        self.schedule_start = None
        self.schedule_end = None
        self.event_filter = None
        self.constraint = None
        self.period = None
        self.evaluations = None
        self.method = None
        self.action = []

    def set_description(self, description: str):
        self.description = description

    def set_event(self, event: str):
        self.event = event

    def set_schedule(self, schedule_start: str, schedule_end: str):
        self.schedule_start = schedule_start
        self.schedule_end = schedule_end

    def set_target_filter(self, event_filter: EventFilterDefinition):
        self.event_filter = event_filter

    def set_constraint(self, constraint: ConditionClauseDefinition):
        self.constraint = constraint

    def set_period(self, period: str):
        self.period = period

    def set_evaluations(self, evaluations: str):
        self.evaluations = evaluations

    def set_method(self, method: str):
        self.method = method

    def add_action(self, action: str):
        self.action.append(action)


def trigger_definition_parser(name: str, data: dict) -> TriggerDefinition:
    trigger = TriggerDefinition(name)
    if data.get('description'):
        description = description_parser(data)
        trigger.set_description(description)
    if data.get('event'):
        trigger.set_event(data.get('event'))
    else:
        abort(400)
    if data.get('schedule'):
        schedule = data.get('schedule')
        trigger.set_schedule(schedule['start_time'], schedule['end_time'])
    if data.get('target_filter'):
        event_filter = data.get('target_filter')
        trigger.set_target_filter(EventFilterDefinition(event_filter.get('node'), event_filter.get('requirement'),
                                                        event_filter.get('capability')))
    if data.get('condition'):
        condition = data.get('condition')
        if type(condition) == dict:
            if condition.get('constraint'):
                constraint = condition.get('constraint')
                trigger.set_constraint(condition_clause_definition_parser('constraint', {'constraint': constraint} ))
            if condition.get('period'):
                trigger.set_period(condition.get('period'))
            if condition.get('evaluations'):
                trigger.set_evaluations(condition.get('evaluations'))
            if condition.get('method'):
                trigger.set_method(condition.get('method'))
        else:
            trigger.set_constraint(condition_clause_definition_parser('condition', {'condition': condition}))
    if data.get('action'):
        for action in data.get('action'):
            trigger.add_action(activity_definition_parser(action))
    return trigger
