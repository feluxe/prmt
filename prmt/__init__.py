"""
This lib is all about asking the user for CLI input.
This file contains public functions only. Private stuff does not belong here.

This module is written with this import style in mind:

    from ompy.cli.prompt import utils as prompt

    prompt.confirm()

"""

from typing import Union, Any, Optional


def string(
    question: str,
    default: str = None,
    force_value: bool = False,
    one_line: bool = False
    ) -> str:
    """
    Ask user question and return input from user.
    @default: Is displayed before the prompt. (optional)
    @force_value: If this is set, the prompt will repeat itself if the user enters an empty string.
    """
    _default: str = '[' + default + '] > ' if default else '> '
    question_line: str = '# ' + question
    prompt_line: str = _default if not one_line else question + ' ' + _default

    print('\n' + question_line) if not one_line else print('')

    answer: str = input(prompt_line) or default

    if force_value and answer == '' or answer is None:
        print('\nInvalid input.')
        answer = string(question, default, force_value, one_line)

    print('')
    return answer


def confirm(
    question: str,
    default: str = None,
    one_line: bool = False
    ) -> bool:
    """
    Ask user question to which she has to anwser with y or n and return a bool.
    @default: Is displayed before the prompt. (optional)
    """
    default_: str = '[' + default + '] > ' if default else '> '
    question_line: str = '# ' + question
    prompt_line: str = default_ if not one_line else question + ' ' + default_

    print('\n' + question_line) if not one_line else print('')

    answer = a = input(prompt_line) or default

    if answer and answer.lower() in ['y', 'yes', 'true', '1']:
        return_val: bool = True
    elif answer and answer.lower() in ['n', 'no', 'false', '0']:
        return_val: bool = False
    else:
        return_val: bool = confirm(question, default, one_line)

    print('')
    return return_val


def _convert_if_dict(item: Union[dict, list]) -> list:
    return list(item.keys()) if isinstance(item, dict) else item


def select(
    question: str,
    options: Union[dict, list],
    return_value: Optional[bool] = True,
    sort: Optional[bool] = True,
    default: Optional[str] = None
    ) -> Union[str, int]:
    """
    Ask user a question and list options to choose from.
    @return_value: If False: func returns selected int (the key).
                   If True: func returns the value as a string.
    """
    prompt = lambda inp: inp if valid(inp) else (print('\nInvalid input.\n'), prompt(input('> ')))[
        1]
    valid = lambda _input: _input and _input.isdigit() and int(_input) in range(len(options))
    _sort = lambda opt: sorted(opt) if sort else opt

    options_: list = _sort(_convert_if_dict(options))
    _default: str = '[' + default + '] > ' if default else '> '

    print('\n# ' + question), [print('#    {}) {}'.format(i, o)) for i, o in enumerate(options_)]

    selection: str = prompt(input(_default) or default)

    print('')

    return int(selection) if not return_value else options_[int(selection)]


def path(
    question: str,
    options: Union[list, dict] = None
    ) -> str:
    """
    Ask user to choose a path from a list or enter a new one.
    If no option is provided, she will be ask to enter a new path immediately.
    TODO: Not sure if types are correct here.
    TODO: Maybe this needs to get refactored.
    """
    option: str = 'Define a PATH manually.'
    options_: Optional[list] = [option] + options if options else None
    selection: Optional[int] = None if not options_ else select(question, options_,
        return_value=False, sort=False)

    print(question) if not selection and not isinstance(selection, int) else None

    q: str = 'Please enter a PATH:'
    result: str = string(q, force_value=True) if selection in (0, None) else options[
        selection]

    print('')

    return result


def list_(
    question: str,
    default: Optional[Union[list, str]] = None,
    one_line: Optional[bool] = None
    ) -> list:
    """
    Ask user for a list of strings. Each one must be separated with a comma.
    """
    info: str = ' (Separate items with a comma.)'
    _question: str = question + info
    _default: str = ', '.join(list(default)) if default else None
    answer: Optional[str] = string(_question, _default, one_line=one_line)

    return [item.strip() for item in answer.split(',')] if answer else []
