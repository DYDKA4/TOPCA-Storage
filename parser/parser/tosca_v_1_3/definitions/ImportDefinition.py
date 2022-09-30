# Single-line grammar:
# imports:
#   - <URI_1>
#   - <URI_2>

# Multi-line grammar
# imports:
#   - file: <file_URI> Required
#     repository: <repository_name>
#     namespace_uri: <definition_namespace_uri>  # deprecated
#     namespace_prefix: <definition_namespace_prefix>
import inspect

from parser.parser import ParserException


class ImportDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'ImportDefinition'
        self.file = None
        self.repository = None
        self.namespace_uri = None
        self.namespace_prefix = None

    def set_file(self, file: str):
        self.file = file

    def set_repository(self, repository: str):
        self.repository = repository

    def set_namespace_uri(self, namespace_uri: str):
        self.namespace_uri = namespace_uri

    def set_namespace_prefix(self, namespace_prefix: str):
        self.namespace_prefix = namespace_prefix


def import_definition_parser(data) -> ImportDefinition:
    import_definition = ImportDefinition()
    if type(data) == str:
        import_definition.set_file(data)
        return import_definition
    if data.get('file'):
        import_definition.set_file(data.get('file'))
    else:
        raise ParserException(400, inspect.stack()[0][3] + ': no_file')
    if data.get('repository'):
        import_definition.set_repository(data.get('repository'))
    if data.get('namespace_uri'):
        import_definition.set_namespace_uri(data.get('namespace_uri'))
    if data.get('namespace_prefix'):
        import_definition.set_namespace_prefix(data.get('namespace_prefix'))
    return import_definition
