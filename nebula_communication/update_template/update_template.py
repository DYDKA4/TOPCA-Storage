from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import update_vertex, fetch_vertex


def update_template(cluster_name: str, value, value_name, varargs: list):
    cluster_vid = '"' + cluster_name + '"'
    value = '"' + value + '"'
    if varargs:
        for var in varargs:
            print(var)
    else:
        vertex_value = fetch_vertex(cluster_vid, 'ServiceTemplateDefinition')
        vertex_value = vertex_value.as_map()
        if value_name not in vertex_value.keys():
            abort(400)
        update_vertex('ServiceTemplateDefinition', cluster_vid, value_name, value)
