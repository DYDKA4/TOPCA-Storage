from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import update_vertex, fetch_vertex
from nebula_communication.update_template.Definition.ImportDefinitionUpdater import update_import_definition
from nebula_communication.update_template.Definition.RepositoryDefinitionUpdater import update_repository_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_template(cluster_name: str, value, value_name, varargs: list):
    cluster_vid = '"' + cluster_name + '"'
    value = '"' + value + '"'
    if len(varargs) == 0:
        vertex_value = fetch_vertex(cluster_vid, 'ServiceTemplateDefinition')
        vertex_value = vertex_value.as_map()
        if value_name not in vertex_value.keys():
            abort(400)
        update_vertex('ServiceTemplateDefinition', cluster_vid, value_name, value)
    elif varargs[0] == 'metadata':
        update_metadata(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'repositories':
        update_repository_definition(cluster_vid, value, value_name, varargs)
    elif varargs[0] == 'imports':
        update_import_definition(cluster_vid, value, value_name, varargs)
    else:
        abort(400)


update_template('cluster', 'new_repository', 'repository', ['imports', 'URI_0'])
