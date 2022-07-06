import logging

import redis

from nebula_communication.nebula_functions import delete_vertex, start_session

r = redis.Redis(host='10.100.151.128', port=6380, db=0)


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


def delete_all():
    session = start_session()
    on_delete = ''
    count = 0
    for it in r.scan_iter('*'):
        if on_delete == '':
            on_delete = '"' + it.decode("utf-8") + '"'
            count += 1
        else:
            on_delete += ', "' + it.decode("utf-8") + '"'
            count += 1
    delete_vertex(session, on_delete)
    logging.info(f'Success of deleting {count}')
    session.release()
    for it in r.scan_iter('*'):
        r.delete(it)
