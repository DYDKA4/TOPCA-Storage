import ard
import puccini.tosca
import sys
import subprocess as sp
import yaml


# try:
#     clout = puccini.tosca.compile('https://raw.githubusercontent.com/Shishqa/clouni-substitution-mapping-sandbox/refactor-templates/tosca-server-example.yaml') # can also be a URL
#     ard.write(clout, sys.stdout)
# except puccini.tosca.Problems as e:
#     print('Problems:', file=sys.stderr)
#     for problem in e.problems:
#         ard.write(problem, sys.stderr)

def parse(path, phases=5):
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

res = parse('https://raw.githubusercontent.com/Shishqa/clouni-substitution-mapping-sandbox/refactor-templates/tosca-server-example.yaml')

print(yaml.dump(res))