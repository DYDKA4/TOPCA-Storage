import inspect


from parser_nebula.parser import ParserException


def link_with_list(list_of_smt, current_template, name_of_connection):
    list_of_smt = list(set(list_of_smt))
    if getattr(current_template, name_of_connection) is None:
        return
    setattr(current_template, name_of_connection, list(set(getattr(current_template, name_of_connection))))
    target_structure = []
    for item in list_of_smt:
        for source in getattr(current_template, name_of_connection):
            if item.name == source and item not in target_structure:
                target_structure.append(item)
                break
    if len(target_structure) != len(getattr(current_template, name_of_connection)):
        print(name_of_connection, getattr(current_template, name_of_connection))
        raise ParserException(400, f'{inspect.stack()[0][3]}: '
                                   f'len(target_structure) != len(getattr(current_template, name_of_connection))')
    setattr(current_template, name_of_connection, {name_of_connection: [current_template, target_structure]})


def link_valid_target_types(target_types, current_template):
    link_with_list(target_types, current_template, 'valid_target_types')


def link_valid_source_types(source_types, current_template):
    link_with_list(source_types, current_template, 'valid_source_types')


def link_members(members, current_template):
    link_with_list(members, current_template, 'members')
