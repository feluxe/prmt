"""
This lib is all about asking the user for Command Line input.
"""

from typing import Union, Any, Optional
import tempfile
import os
from subprocess import call


def _print_margin(int_):
    for i in range(0, int_):
        print()


def editor_input(prompt):
    editor = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vi'

    print(prompt, end='')

    with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+') as tmp_file:
        tmp_file.write('')
        tmp_file.flush()
        call([editor, tmp_file.name])
        tmp_file.seek(0)
        edited_message = tmp_file.read()

    print(edited_message)

    return edited_message


def string(
    question: str,
    default: str = None,
    margin=(0, 1),
    force_val: bool = False,
    editor=False,
) -> str:
    """
    Ask user question and return input from user.
    @default: Is displayed before the prompt and used if an empty string was passed.
    @force_value: Repeat if input is empty.
    @margin: Add a margin before and after the question.
    """
    _print_margin(margin[0])

    default_view: str = '[{}]: '.format(str(default)) if default else ''
    prompt: str = question + default_view

    if editor:
        answer = editor_input(prompt) or default

    else:
        answer: str = input(prompt) or default

    if force_val and not answer:
        print('\nInvalid input.')

        answer = string(
            question=question,
            default=default,
            margin=margin,
            force_val=force_val,
            editor=editor
        )

    else:
        _print_margin(margin[1])

    return answer


def confirm(
    question: str,
    default: str = None,
    margin=(0, 1),
) -> bool:
    """
    Ask user question to which she has to answer with y or n and return a bool.
    @default: Is displayed before the prompt. (optional)
    """
    _print_margin(margin[0])

    default_view: str = '[{}]: '.format(str(default)) if default else ''
    prompt: str = question + default_view

    answer: str = input(prompt) or default

    if answer and answer.lower() in ['y', 'yes', 'true', '1']:
        return_val: bool = True

    elif answer and answer.lower() in ['n', 'no', 'false', '0']:
        return_val: bool = False

    else:
        return_val: bool = confirm(
            question=question,
            default=default,
            margin=margin
        )

    _print_margin(margin[1])

    return return_val


def _validate_selection(selection, len_options):
    return selection \
           and str(selection).isdigit() \
           and int(selection) in range(len_options)


def select(
    question: str,
    options: Union[dict, list],
    default: Optional[str] = None,
    margin=(0, 1),
    return_val: Optional[bool] = True,
    sort: Optional[bool] = True,
) -> Union[str, int]:
    """
    Ask user a question and list options to choose from.
    @return_val: If False: func returns selected int (the key).
                 If True: func returns the value as a string.
    """
    _print_margin(margin[0])

    options: list = list(options.keys()) if isinstance(options, dict) else options
    options: list = sorted(options) if sort else options
    default_view: str = '[{}]: '.format(str(default)) if default else ''

    print(question)

    for i, o in enumerate(options):
        print('  {}) {}'.format(i, o))

    selection: str = input(default_view) or default

    if not _validate_selection(selection, len(options)):
        selection: str = select(
            question=question,
            options=options,
            default=default,
            margin=margin,
            return_val=False,
            sort=sort
        )

    else:
        _print_margin(margin[1])

    return int(selection) \
        if not return_val \
        else options[int(selection)]


def path(
    question: str,
    options: Union[list, dict] = None,
    default: Optional[str] = None,
    margin=(0, 1),
) -> str:
    """
    Ask user to choose a path from a list or enter a new one.
    If no option is provided, she will be ask to enter a new path immediately.
    """
    option: str = 'Enter PATH manually.'
    options_: Optional[list] = [option] + options if options else None

    if options:
        selection: Optional[int] = select(
            question=question,
            options=options_,
            default=default,
            return_val=False,
            margin=margin,
            sort=False
        )

    else:
        selection: Optional[int] = None

    if not selection and not isinstance(selection, int):
        print(question)

    if selection in (0, None):
        result: str = string(
            question='Please enter a PATH:\n',
            margin=margin,
            force_val=True
        )

    else:
        result: str = options[selection]

    return result


def list_(
    question: str,
    default: Optional[Union[list, str]] = None,
    margin=(0, 1),
    force_val: bool = False,
) -> list:
    """
    Ask user for a list of strings. Each one must be separated with a comma.
    """
    default_: str = ', '.join(list(default)) if default else None

    answer: Optional[str] = string(
        question=question,
        default=default_,
        margin=margin,
        force_val=force_val
    )

    if answer:
        return [item.strip() for item in answer.split(',')]

    else:
        return []
