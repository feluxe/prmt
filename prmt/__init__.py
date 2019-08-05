"""
This lib is all about asking the user for Command Line input.
"""

from typing import Union, Any, Optional, Tuple, List
import tempfile
import os
import subprocess as sp


def get_input_from_texteditor(
    instruction=None,
    default=None,
    file_type=None,
    remove_comments=True,
) -> str:

    if default:
        q = f"{default}\n"
    else:
        q = "\n"

    if instruction is None and remove_comments == True:
        q += "# Lines starting with '#' will be ignored.\n"
    elif isinstance(instruction, str):
        for line in instruction.splitlines():
            q += f"# {line}\n"

    editor = os.environ.get('EDITOR') or 'vi'

    with tempfile.NamedTemporaryFile(
        suffix=file_type or "", mode='w+'
    ) as tmp_file:
        tmp_file.write(q)
        tmp_file.flush()

        if editor in ['vi', 'vim'] and file_type:
            sp.run([editor, '-c', f'set filetype={file_type}', tmp_file.name])
        else:
            sp.run([editor, tmp_file.name])

        tmp_file.seek(0)

        user_input_raw = tmp_file.read()

    user_input_clean = ''

    if q:
        user_input_clean = user_input_raw.replace(q, '')
    else:
        user_input_clean = user_input_raw

    print(user_input_clean)

    return user_input_clean


def _string_base(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
    blacklist: Optional[list] = None,
    open_editor: bool = False,
    editor_instruction: Optional[str] = None,
    editor_file_type=None,
    editor_remove_comments=True,
) -> str:
    """
    Ask user question and return input from user.

    :param question: Question to ask.
    :param default: Add default value.
    :param fmt: Set prompt formatting.
    :param blacklist: Retry if user input is found in 'blacklist'.
    :param open_editor: If 'True' opens editor for the user to enter the string.
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
        answer = get_input_from_texteditor(
            instruction=editor_instruction,
            default=default,
            file_type=editor_file_type,
            remove_comments=editor_remove_comments,
        ) or default or ''
    else:
        answer = input(prompt) or default or ''

    if blacklist and answer in blacklist:

        print('Invalid input.' + fmt_end)

        answer = _string_base(
            question=question,
            default=default,
            fmt=fmt,
            blacklist=blacklist,
            open_editor=open_editor,
            editor_instruction=editor_instruction,
        )
    else:
        print(fmt_end, end='')

    return answer


def string_from_editor(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
    blacklist: Optional[list] = None,
    instruction: Optional[str] = None,
    file_type=None,
) -> str:
    return _string_base(
        question=question,
        default=default,
        fmt=fmt,
        blacklist=blacklist,
        open_editor=True,
        editor_instruction=instruction,
        editor_file_type=file_type,
    )


def string(
    question: str,
    default: Optional[str] = None,
    fmt: List[str] = None,
    blacklist: Optional[list] = None,
) -> str:
    return _string_base(
        question=question,
        default=default,
        fmt=fmt,
        blacklist=blacklist,
        open_editor=False
    )


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
