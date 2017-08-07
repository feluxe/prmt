import sys
import os
from ompy.app.utils import load_yaml
from ompy.cli.styling import tags
from ompy.cli.prompt.sequences import publish as prompt_seq_publish
from ompy.cmdlib import build
from ompy.cmdlib import git
from ompy.build.semver import get_python_wheel_name_from_semver_num, convert_semver_to_wheelver
from ompy.datastruc import AttrDict

CWD = os.getcwd()
CFG_FILE = CWD + '/CONFIG.yaml'
CFG = load_yaml(CFG_FILE, keep_order=True)


def publish_sequence() -> None:
    print(tags.h2('Publish'))

    kwargs = {
        'ask_build': True,
        'ask_registry': True,
        'cur_version': CFG['version'],
        'gemfury_env': CFG['gemfury_env'],
        }

    answers: AttrDict = prompt_seq_publish.default_args(**kwargs)
    results = list()

    if answers.should_update_version_num:
        results.append(build.update_version_num_in_cfg_yaml(CFG_FILE, answers.version))

    if answers.should_run_build_py:
        results.append(build.run_build_file(CWD + '/build.py'))

    if answers.should_run_git_commands:
        if answers.should_run_git_add_all:
            results.append(git.add_all())

        if answers.should_run_git_commit:
            results.append(git.commit(answers.commit_msg))

        if answers.should_run_git_tag:
            results.append(git.tag(answers.version, answers.branch))

        if answers.should_run_git_push:
            results.append(git.push(answers.branch))

    if answers.should_push_registry:
        if answers.should_push_gemfury:
            wheel_version_num = convert_semver_to_wheelver(answers.version)
            wheel_file = get_python_wheel_name_from_semver_num(wheel_version_num, CWD + '/dist')
            results.append(build.push_python_wheel_to_gemfury('dist/' + wheel_file))

    print(tags.h3('Publish Results'))
    for item in results:
        print(item.return_msg)


def execute() -> None:
    try:
        publish_sequence()
    except KeyboardInterrupt:
        print('\n\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


if __name__ == '__main__':
    execute()
