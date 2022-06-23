from werkzeug.exceptions import abort


def link_with_list(list_of_smt, current_template, name_of_connection):
    if getattr(current_template, name_of_connection) is None:
        return
    target_structure = []
    for item in list_of_smt:
        for source in getattr(current_template, name_of_connection):
            if item.name == source:
                target_structure.append(item)
                break
    if len(target_structure) != len(getattr(current_template, name_of_connection)):
        abort(400)
    current_template.valid_target_types = {'valid_target_types': [current_template, target_structure]}


def link_valid_target_types(target_types, current_template):
    link_with_list(target_types, current_template, 'valid_target_types')


def link_valid_source_types(source_types, current_template):
    link_with_list(source_types, current_template, 'valid_source_types')


def link_members(members, current_template):
    link_with_list(members, current_template, 'members')
