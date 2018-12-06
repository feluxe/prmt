"""
This lib is all about asking the user for Command Line input.
"""

from typing import Union, Any, Optional, Tuple, List
import tempfile
import os
from subprocess import call


def get_input_from_texteditor(
    question=None,
    default=None,
) -> str:

    q_commented = ''

    if question:
        q_commented += "# NOTE:\n"
        q_commented += "# This comment will be removed. Don't change it.\n"
        q_commented += "#\n"
        q_commented += "# QUESTION:\n"

        for line in question.splitlines():
            q_commented += '# ' + line + '\n'

    if default:
        q_commented += '#\n# DEFAULT:\n'
        q_commented += '# ' + default
        q_commented += '\n'

    editor = os.environ.get('EDITOR') or 'vi'

    with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+') as tmp_file:
        tmp_file.write(q_commented)
        tmp_file.flush()
        call([editor, tmp_file.name])
        tmp_file.seek(0)
        user_input_raw = tmp_file.read()

    user_input_clean = ''

    if q_commented:
        user_input_clean = user_input_raw.replace(q_commented, '')

    else:
        user_input_clean = user_input_raw

    print(user_input_clean)

    return user_input_clean


def string(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
    blacklist: Optional[list] = None,
    open_editor: bool = False,
) -> str:
    """
    Ask user question and return input from user.

    @question: Question to ask.
    @default: Add default value.
    @fmt: Set prompt formatting.
    @blacklist: Retry if user input is found in 'blacklist'.
    @open_editor: If 'True' opens editor for the user to enter the string.

    """
    if not fmt:
        fmt = ['\n{}\n', '[{}] ', '> {}\n']

    fmt_question = fmt[0]
    fmt_default = fmt[1]
    fmt_prompt = fmt[2].split('{}')[0]
    fmt_end = fmt[2].split('{}')[1]

    prompt = ''

    if default:
        prompt = fmt_question.format(question) +\
                 fmt_default.format(default) +\
                 fmt_prompt
    else:
        prompt = fmt_question.format(question) + fmt_prompt

    if open_editor:

        print(prompt, end='')
        answer = get_input_from_texteditor(question, default) or default or ''

    else:
        answer = input(prompt) or default or ''

    if blacklist and answer in blacklist:

        print('Invalid input.' + fmt_end)

        answer = string(
            question=question,
            default=default,
            fmt=fmt,
            blacklist=blacklist,
            open_editor=open_editor,
        )

    else:
        print(fmt_end, end='')

    return answer


def integer(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
    blacklist: Optional[List[int]] = None,
) -> Union[int, None]:
    """
    Ask user question to which she has to enter an integer.

    @question: Question to ask.
    @default: Add default value.
    @fmt: Set prompt formatting.
    @blacklist: Retry if user input is found in 'blacklist'.
    """

    if not fmt:
        fmt = ['\n{}\n', '[{}] ', '> {}\n']

    fmt_question = fmt[0]
    fmt_default = fmt[1]
    fmt_prompt = fmt[2].split('{}')[0]
    fmt_end = fmt[2].split('{}')[1]

    if default:
        prompt = fmt_question.format(question) +\
                 fmt_default.format(default) +\
                 fmt_prompt
    else:
        prompt = fmt_question.format(question) + fmt_prompt

    answer: str = input(prompt) or default or ''

    print(fmt_end, end='')

    retry = False
    return_val: Union[int, None]

    if answer:
        try:
            return_val = int(answer)
        except ValueError:
            retry = True
    else:
        return_val = None

    if not retry and blacklist:
        if return_val in blacklist:
            retry = True

    if retry:

        print("Invalid input." + fmt_end)

        return_val = integer(
            question=question,
            default=default,
            fmt=fmt,
            blacklist=blacklist,
        )

    return return_val


def confirm(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
) -> bool:
    """
    Ask user question to which she has to answer with y or n and return a bool.

    @question: Question to ask.
    @default: Add default value.
    @fmt: Set prompt formatting.
    @blacklist: Retry if user input is found in 'blacklist'.
    """

    if not fmt:
        fmt = ['\n{}\n', '[{}] ', '> {}\n']

    fmt_question = fmt[0]
    fmt_default = fmt[1]
    fmt_prompt = fmt[2].split('{}')[0]
    fmt_end = fmt[2].split('{}')[1]

    if default:
        prompt = fmt_question.format(question) +\
                 fmt_default.format(default) +\
                 fmt_prompt
    else:
        prompt = fmt_question.format(question) + fmt_prompt

    return_val = None

    answer: str = input(prompt) or default or ''

    print(fmt_end, end='')

    if answer and answer.lower() in ['y', 'yes', 'true', '1']:
        return_val = True

    elif answer and answer.lower() in ['n', 'no', 'false', '0']:
        return_val = False

    else:
        return_val = confirm(
            question=question,
            default=default,
            fmt=fmt,
        )

    return return_val


def select(
    question: str,
    options: Union[dict, list, tuple],
    default: Optional[str] = None,
    fmt: List[str] = None,
    custom_key: Optional[Union[str, int]] = None,
    custom_fmt=['\n{}\n', '{}', '> {}'],
) -> Tuple[Union[int, str], Any]:
    """
    Ask user a question and list options to choose from, return the seleced
    key, value pair.

    @question: Question to ask.
    @options: The options which the user can choose from.
    @default: Add default value.
    @fmt: Set prompt formatting.
    @custom_key: If the user selects this key, she can type in a custom value.
    @custom_fmt: Set formatting for the custom value prompt.

    """

    if not fmt:
        fmt = ['\n{}\n', '  {}: {}', '\n', '[{}] ', '> {}\n']

    fmt_question = fmt[0]
    fmt_option = fmt[1]
    fmt_post_option = fmt[2]
    fmt_default = fmt[3]
    fmt_prompt = fmt[4].split('{}')[0]
    fmt_end = fmt[4].split('{}')[1]

    if default:
        prompt = fmt_post_option +\
                 fmt_default.format(default) +\
                 fmt_prompt
    else:
        prompt = fmt_post_option + fmt_prompt

    print(fmt_question.format(question))

    # Print Options

    if isinstance(options, (list, tuple)):

        for key, option in enumerate(options):
            print(fmt_option.format(key, str(option)))

    elif isinstance(options, dict):

        for key, option in options.items():
            print('  {}: {}'.format(key, str(option)))

    # Let User Choose Option

    selected_key: Union[int, str] = input(prompt) or str(default)

    # Validate Input
    retry = True

    if isinstance(options, (list, tuple)):

        try:
            selected_key = int(selected_key)
            selected_value = options[int(selected_key)]
            retry = False
        except (ValueError, IndexError):
            pass

    elif isinstance(options, dict):

        try:
            selected_value = options[selected_key]
            retry = False
        except KeyError:
            try:
                selected_key = int(selected_key)
                selected_value = options[selected_key]
                retry = False
            except ValueError:
                pass
            except KeyError:
                pass

    if not retry and custom_key and str(selected_key) == str(custom_key):
        selected_value = string(selected_value, fmt=custom_fmt)

    # If Input Invalid, recurse.
    print(fmt_end, end='')

    if retry:
        selected_key, selected_value = select(
            question=question,
            options=options,
            default=default,
            fmt=fmt,
        )

    return selected_key, selected_value


def list_of_str(
    question: str,
    default: Optional[Union[list, str]] = None,
    fmt: List[str] = None,
    blacklist: Optional[list] = None,
) -> list:
    """
    Ask user for a list of strings. Values must be seperated with commas.

    @question: Question to ask.
    @default: Add default value.
    @fmt: Set prompt formatting.
    @blacklist: Retry if user input is found in 'blacklist'.
    """

    if not fmt:
        fmt = ['\n{}\n', '[{}] ', '> {}\n']

    fmt_end = fmt[2].split('{}')[1]

    if isinstance(default, (list, tuple)):
        default = ', '.join(default)

    answer = string(
        question=question,
        default=default,
        fmt=fmt,
        blacklist=None,
    )

    retry = False

    return_val = [item.strip() for item in answer.split(',')]

    if blacklist:
        for item in return_val:
            if item in blacklist:
                retry = True

    if retry:

        print('Invalid input.' + fmt_end)

        return_val = list_of_str(
            question=question,
            default=default,
            fmt=fmt,
            blacklist=blacklist,
        )

    return return_val