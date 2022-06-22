from werkzeug.exceptions import abort


def link_valid_target_types(target_types, current_template):
    if current_template.valid_target_types is None:
        return
    target_structure = []
    for target_type in target_types:
        for source in current_template.valid_target_types:
            if target_type.name == source:
                target_structure.append(target_type)
                break
    if len(target_structure) != len(current_template.valid_target_types):
        abort(400)
    current_template.valid_target_types = {'valid_target_types': [current_template, target_structure]}


def link_valid_source_types(source_types, current_template):
    if current_template.valid_source_types is None:
        return
    source_structure = []
    for source_type in source_types:
        for source in current_template.valid_source_types:
            if source_type.name == source:
                source_structure.append(source_type)
                break
    if len(source_structure) != len(current_template.valid_source_types):
        abort(400)
    current_template.valid_source_types = {'valid_source_types': [current_template, source_structure]}


def link_members(members, current_template):
    if current_template.valid_source_types is None:
        return
    members_structure = []
    for member in members:
        for source in current_template.valid_source_types:
            if member.name == source:
                members_structure.append(member)
                break
    if len(members_structure) != len(current_template.valid_source_types):
        abort(400)
    current_template.valid_source_types = {'valid_source_types': [current_template, members_structure]}
