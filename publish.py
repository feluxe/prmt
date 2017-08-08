import sys
import os
from buildlib.utils.yaml import load_yaml
from buildlib.cmds.sequences.publish import publish_sequence

CWD = os.getcwd()
CFG_FILE = CWD + '/CONFIG.yaml'
CFG = load_yaml(CFG_FILE, keep_order=True)
cur_version = CFG['version']


def publish() -> None:
    publish_sequence(
        cfg_file=CFG_FILE,
        build_file=CWD + '/build.py',
        wheel_dir=CWD + '/dist',
        cur_version=cur_version,
        run_update_version='y',
        run_push_gemfury='y',
        )


def execute() -> None:
    try:
        publish()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


if __name__ == '__main__':
    execute()
