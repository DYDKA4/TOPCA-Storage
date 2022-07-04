import redis

r = redis.Redis(host='10.100.151.128', port=6380, db=0)


def add_vid(vid, cluster_name):
    result = r.get(vid)
    if result is not None:
        print(result)
        return True
    r.set(vid, cluster_name)
    return False