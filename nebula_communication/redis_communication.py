import logging

from nebula_communication import r


def add_vid(vid, cluster_name):
    result = r.get(vid)
    if result is not None:
        print(result)
        return True
    r.set(vid, cluster_name)
    return False


def del_all_by_service_template_name(name):
    for it in r.scan_iter('*'):
        if r.get(it) == name:
            del_by_vid(it)


def del_by_vid(vid):
    r.delete(vid)


def get_all_vid_from_cluster(cluster_name):
    clusters_vid = []
    for it in r.scan_iter('*'):
        if r.get(it).decode("utf-8") == cluster_name:
            clusters_vid.append(it.decode("utf-8"))
    return clusters_vid


def get_cluster_name_from_redis(vid):
    return r.get(vid).decode("utf-8")
