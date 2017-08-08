import sys
import os
from headlines import h2, h3
from buildlib.utils.yaml import load_yaml
from buildlib.cmds.build import build_python_wheel

CWD = os.getcwd()
CFG = load_yaml(CWD + '/CONFIG.yaml', keep_order=True)


def build_sequence() -> None:
    print(h2('Build'))

    result = []

    result.append(build_python_wheel(clean_dir=True))

    print(h3('Build Results'))
    for command in result:
        print(command.return_msg)


def execute() -> None:
    try:
        build_sequence()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


if __name__ == '__main__':
    execute()
