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

from app.parser.tosca_v_1_3.ConditionClauseDefinition import ConditionClauseDefinition, \
    condition_clause_definition_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.EventFilterDefinition import EventFilterDefinition


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
        self.condition = None
        self.action = None

    def set_description(self, description: str):
        self.description = description

    def set_event(self, event: str):
        self.event = event

    def set_schedule(self, schedule_start: str, schedule_end: str):
        self.schedule_start = schedule_start
        self.schedule_end = schedule_end

    def set_event_filter(self, event_filter: EventFilterDefinition):
        self.event_filter = event_filter

    def set_constraint(self, constraint: ConditionClauseDefinition):
        self.constraint = constraint

    def set_period(self, period: str):
        self.period = period

    def set_evaluations(self, evaluations: str):
        self.evaluations = evaluations

    def set_method(self, method: str):
        self.method = method

    def set_condition(self, condition: str):
        self.condition = condition

    def set_action(self, action: str):
        self.action = action


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
        trigger.set_event_filter(EventFilterDefinition(event_filter.get('node'), event_filter.get('requirement'),
                                                       event_filter.get('capability')))
    short_notation = True
    if data.get('condition'):
        condition = data.get('condition')
        if condition.get('constraint'):
            short_notation = False
            trigger.set_constraint(condition_clause_definition_parser('constraint', condition.get('constraint')))
        if condition.get('period'):
            short_notation = False
            trigger.set_period(condition.get('period'))
        if condition.get('evaluations'):
            short_notation = False
            trigger.set_evaluations(condition.get('evaluations'))
        if condition.get('method'):
            short_notation = False
            trigger.set_method(condition.get('method'))
        if short_notation:
            trigger.set_condition(condition)
    if data.get('action'):
        trigger.set_action(str(data.get('action')))
    return trigger
