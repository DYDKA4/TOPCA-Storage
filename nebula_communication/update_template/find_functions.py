from nebula_communication.nebula_functions import find_destination, fetch_vertex


def form_result(vid_to_update, value_name):
    result = find_destination(vid_to_update, value_name)
    if result:
        return result[0].as_string()
    else:
        return None


def return_all(value, value_name, destination, varargs, length):
    if destination is None:
        return None, len(varargs) == length
    if not value or not value_name:
        result = []
        for vid in destination:
            result.append(vid.as_string())
        return result, len(varargs) == length,
    return None, False


def get_names(list_of_vid: list, vertex_type):
    answer = {}
    for vid in list_of_vid:
        result = fetch_vertex('"'+vid+'"', vertex_type)
        result = result.as_map().get('name').as_string()
        answer[vid] = result
    return answer


def get_attribute(vid, vertex_type, value_name):
    if value_name == 'value':
        value_name = 'values'
    result = fetch_vertex('"' + vid + '"', vertex_type)
    result = result.as_map().get(value_name).as_string()
    return result