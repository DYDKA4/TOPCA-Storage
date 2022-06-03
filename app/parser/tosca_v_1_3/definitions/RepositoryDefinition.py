# Single-line grammar (no credential):
# <repository_name>: <repository_address>

# Multi-line grammar
# <repository_name>:
#   description: <repository_description>
#   url: <repository_address> Required
#   credential: <authorization_credential> #todo Make support of tosca.datatypes.Credential?
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser


class RepositoryDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'RepositoryDefinition'
        self.url = None
        self.description = None
        self.credential = None

    def set_url(self, url: str):
        self.url = url

    def set_description(self, description: str):
        self.description = description

    def set_credential(self, credential: str):
        self.credential = credential


def repository_definition_parser(name: str, data: dict) -> RepositoryDefinition:
    repository = RepositoryDefinition(name)
    if type(data) == str:
        repository.set_url(str(data))
        return repository
    if data.get('url'):
        repository.set_url(data.get('url'))
    else:
        abort(400)
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            repository.set_description(description)
    if data.get('credential'):
        repository.set_credential(str(data.get('credential')))
    return repository
