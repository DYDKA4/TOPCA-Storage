import yaml
from flask import jsonify

from nebula_communication import session
from nebula_communication.nebula_functions import find_vertex_by_properties, find_path
from nebula_communication.template_builder.type.NodeTypes import construct_node_type


def find_all_dependencies(node_name):
    vertexes = find_vertex_by_properties('NodeType', name=node_name)
    if vertexes is None:
        return jsonify({'status': 200,
                        'result': None})
    result = find_path(str(vertexes.column_values('id'))[1:-1], '"Jupyter_1"', type_path='REVERSELY')
    result = result.column_values('p')[0].as_path().start_node().get_id()
    ans = construct_node_type([result], None)
    print(yaml.dump(ans, default_flow_style=False))

    return jsonify({'status': 200})


find_all_dependencies('michman.nodes.Jupyter.Jupyter-6-0-1')
session.close()