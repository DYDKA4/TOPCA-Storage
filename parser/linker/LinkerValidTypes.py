from werkzeug.exceptions import abort


def link_valid_target_types(target_types, current_template):
    if current_template.valid_target_types is None:
        return
    valid_target_types = {'valid_target_types' : []}
    target_structure = []
    for target_type in target_types:
        for source in current_template.valid_target_types:
            if target_type.name == source:
                target_structure.append(target_type)
                break
    if len(target_structure) != len(current_template.valid_target_types):
        abort(400)
    current_template.valid_target_types = {'valid_target_types': [current_template, target_structure]}
