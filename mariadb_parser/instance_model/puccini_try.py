import subprocess as sp
import yaml

def puccini_parse(path, phases=5):
    PUCCINI_CMD = '/home/tulin/go/bin/puccini-tosca parse'
    pipe = sp.Popen(
        f'{PUCCINI_CMD} -s {phases} {path}',
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE
    )
    res = pipe.communicate()

    if pipe.returncode != 0:
        raise RuntimeError(res[1].decode())

    return yaml.safe_load(res[0])

