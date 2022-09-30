import inspect


from parser.parser import ParserException


def link_derived_from(main_template, current_template):
    if current_template.derived_from is None:
        return
    for other_template in main_template:
        if other_template.name == current_template.derived_from:
            current_template.derived_from = {'derived_from': [current_template, other_template]}
            return
    print(main_template, current_template.derived_from)
    raise ParserException(400, f'{inspect.stack()[0][3]}: other_template.name == current_template.derived_from')
