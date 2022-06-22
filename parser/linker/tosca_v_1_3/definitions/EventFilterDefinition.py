# node: <node_type_name> | <node_template_name>
# requirement: <requirement_name>
# capability: <capability_name>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def link_capability_definition(service_template: ServiceTemplateDefinition, event: EventFilterDefinition) -> None:
    if type(event.requirement) == str:
        link_by_type_name(service_template.artifact_types, event, 'requirement')
    if type(event.capability) == str:
        link_by_type_name(service_template.artifact_types, event, 'capability')
    if type(event.node) == str:
        link_by_type_name(service_template.node_types, event, 'node')
    topology_template: TemplateDefinition = service_template.topology_template
    if type(event.node) == str and topology_template:
        link_by_type_name(topology_template.node_templates, event, 'node')
    if str in {type(event.requirement), type(event.capability)}:
        abort(400)
