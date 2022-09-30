# node: <node_type_name> | <node_template_name>
# requirement: <requirement_name>
# capability: <capability_name>
import inspect


from parser.linker.LinkByName import link_by_type_name
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


def link_event_filter_definition(service_template: ServiceTemplateDefinition, event: EventFilterDefinition) -> None:

    topology_template: TemplateDefinition = service_template.topology_template
    node_template = []
    if topology_template.node_templates:
        node_template = topology_template.node_templates
    link_by_type_name(service_template.node_types + node_template, event, 'node')
    if event.node.get('node')[1].vertex_type_system == 'NodeType':
        node_type: NodeType = event.node.get('node')[1]
        link_by_type_name(node_type.requirements, event, 'requirement')
        link_by_type_name(node_type.capabilities, event, 'capability')
    else:
        node_template: NodeTemplate = event.node.get('node')[1]
        link_by_type_name(node_template.requirements, event, 'requirement')
        link_by_type_name(node_template.capabilities, event, 'capability')

    if str in {type(event.node),type(event.requirement), type(event.capability)}:
        raise ParserException(400, inspect.stack()[0][3] +
                              'str in {type(event.node),type(event.requirement), type(event.capability)}')
