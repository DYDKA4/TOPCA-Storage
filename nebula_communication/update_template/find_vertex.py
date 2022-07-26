from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import get_all_vertex, fetch_vertex
from nebula_communication.redis_communication import get_all_vid_from_cluster


def find_vertex(cluster_name, vertex_type_system, search_by, search_by_value):
    if vertex_type_system is None:
        abort(400)
    elif search_by and search_by_value is None:
        abort(400)
    elif search_by is None and search_by_value:
        abort(400)
    if cluster_name is None:
        if search_by is None:
            vid = []
            vid_from_nebula = get_all_vertex(vertex_type_system)
            for vid_tmp in vid_from_nebula:
                vid.append(vid_tmp.as_string())
            return vid
        elif search_by and search_by_value:
            result = []
            vid_from_nebula = get_all_vertex(vertex_type_system)
            for vid in vid_from_nebula:
                vid_value = fetch_vertex(vid, vertex_type_system)
                vid_value = vid_value.as_map()
                if not vid_value.get(search_by).is_null():
                    if vid_value.get(search_by).as_string() == search_by_value:
                        result.append(vid.as_string())
            return result
    elif cluster_name:
        vid_from_nebula = get_all_vertex(vertex_type_system)
        vid = []
        for vid_tmp in vid_from_nebula:
            vid.append(vid_tmp.as_string())
        vid_from_cluster = get_all_vid_from_cluster(cluster_name)
        vid = list(set(vid) & set(vid_from_cluster))
        if search_by is None:
            return vid
        elif search_by and search_by_value:
            for vid in
    vid = None
#
    return vid


res = find_vertex(None, 'PropertyDefinition', 'description', 'test_property_description_0_from_relationship_type')
print(res)