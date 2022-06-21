from werkzeug.exceptions import abort

from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition


def link_by_type_name(main_template, current_template: RequirementDefinition, link_type,
                      attribute_name=None):  # todo Think about it
    if attribute_name is None:
        attribute_name = link_type
    if current_template.__dict__.get(attribute_name) is None:
        return
    for other_template in main_template:
        if other_template.name == current_template.__dict__[attribute_name]:
            setattr(current_template, attribute_name, {link_type: [current_template, other_template]})
            return
    abort(400)


def link_by_relationship_type_name(main_template, current_template):
    if current_template.relationship is None:
        return
    for other_template in main_template:
        if other_template.name == current_template.relationship:
            current_template.relationship = {'relationship': [current_template, other_template]}
            return
    abort(400)


def link_by_capability_type_name(main_template, current_template):
    if current_template.capability is None:
        return
    for other_template in main_template:
        if other_template.name == current_template.capability:
            current_template.capability = {'capability': [current_template, other_template]}
            return
    abort(400)


def link_by_node_type_name(main_template, current_template):
    if current_template.node is None:
        return
    for other_template in main_template:
        if other_template.name == current_template.node:
            current_template.node = {'node': [current_template, other_template]}
            return
    abort(400)
