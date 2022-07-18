import uuid

from nebula_communication.redis_communication import add_vid


def generate_uuid(template, cluster_name):
    template.vid = uuid.uuid4()
    while add_vid(str(template.vid), cluster_name):
        template.vid = uuid.uuid4()
    template.vid = '"' + str(template.vid) + '"'
