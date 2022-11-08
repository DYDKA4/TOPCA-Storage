# Short notation
# <trigger_name>:
#   description: <trigger_description>
#   event: <event_name> Required #todo Maybe link it with smt?
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
#   event: <event_name>
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

from parser_nebula.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import ConditionClauseDefinition, \
    condition_clause_definition_parser
from parser_nebula.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser_nebula.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition

