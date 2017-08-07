import sys
import os
# from ompy.cli.styling import tags
# from ompy.app.utils import load_yaml
# from ompy.cmdlib.build import build_python_wheel

CWD = os.getcwd()
# CFG = load_yaml(CWD + '/CONFIG.yaml', keep_order=True)


def build_sequence() -> None:
    # print(tags.h2('Build'))

    result = []

    # result.append(build_python_wheel(clean_dir=True))

    # print(tags.h3('Build Results'))
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
