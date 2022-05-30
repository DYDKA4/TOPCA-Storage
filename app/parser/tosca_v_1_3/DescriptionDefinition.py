# description: <string>

def description_parser(data: dict) -> str:
    description = str(data.get('description'))
    description = description.replace("\n", " ")
    return description
