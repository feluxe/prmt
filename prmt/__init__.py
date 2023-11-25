"""
A bunch of functions to prompt a user for values on the command line.
"""
from typing import Union, Any, Optional, Tuple, List
import tempfile
import os
import subprocess as sp
import platform
import sys

if platform.system == "Windows":
    import msvcrt
else:
    import termios


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

    editor = os.environ.get("EDITOR") or "vi"

    with tempfile.NamedTemporaryFile(suffix=file_type or "", mode="w+") as tmp_file:
        tmp_file.write(q)
        tmp_file.flush()

        if editor in ["vi", "vim"] and file_type:
            sp.run([editor, "-c", f"set filetype={file_type}", tmp_file.name])
        else:
            sp.run([editor, tmp_file.name])

        tmp_file.seek(0)

        user_input_raw = tmp_file.read()

    user_input_clean = ""

    if q:
        user_input_clean = user_input_raw.replace(q, "")
    else:
        user_input_clean = user_input_raw

    print(user_input_clean)

    return user_input_clean


def read_stdin_non_blocking_windows():
    """
    TODO: This is not tested...
    """
    if msvcrt.kbhit():
        return msvcrt.getch().decode("utf-8")
    else:
        return None


def read_stdin_non_blocking_unix():
    fd = sys.stdin.fileno()
    orig = termios.tcgetattr(fd)

    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0

    try:
        termios.tcsetattr(fd, termios.TCSAFLUSH, new)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, orig)


def read_stdin_non_blocking():
    if platform.system == "Windows":
        return read_stdin_non_blocking_windows()
    else:
        return read_stdin_non_blocking_unix()


def _string_base(
    question: str,
    default: Optional[str] = None,
    blacklist: Optional[list] = None,
    open_editor: bool = False,
    editor_instruction: Optional[str] = None,
    editor_file_type=None,
    editor_remove_comments=True,
    multiline=False,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> str:
    fmt = fmt or [None, None, None]
    fmt_question = fmt_question or fmt[0] or "\n{}\n"
    fmt_default = fmt_default or fmt[1] or "[{}]"
    fmt_prompt = fmt_prompt or fmt[2] or "> {}\n"
    fmt_prompt_start = fmt_prompt.split("{}")[0]
    fmt_prompt_end = fmt_prompt.split("{}")[1]

    prompt = ""

    if default:
        prompt = (
            fmt_question.format(question)
            + fmt_default.format(default)
            + fmt_prompt_start
        )
    else:
        prompt = fmt_question.format(question) + fmt_prompt_start

    if open_editor:
        print(prompt, end="")
        answer = (
            get_input_from_texteditor(
                instruction=editor_instruction,
                default=default,
                file_type=editor_file_type,
                remove_comments=editor_remove_comments,
            )
            or default
            or ""
        )

    elif multiline:
        print(prompt, end="")

        answer = ""

        try:
            while True:
                user_input = read_stdin_non_blocking()
                if user_input is not None:
                    answer += user_input
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass

        answer = answer or default or ""

    else:
        answer = input(prompt) or default or ""

    if blacklist and answer in blacklist:
        print("Invalid input." + fmt_prompt_end)

        answer = _string_base(
            question=question,
            default=default,
            blacklist=blacklist,
            open_editor=open_editor,
            editor_instruction=editor_instruction,
            fmt_question=fmt_question,
            fmt_default=fmt_default,
            fmt_prompt=fmt_prompt,
        )
    else:
        print(fmt_prompt_end, end="")

    return answer


def string_from_editor(
    question: str,
    default: Optional[str] = None,
    blacklist: Optional[list] = None,
    instruction: Optional[str] = None,
    file_type=None,
    remove_comments=True,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> str:
    """
    Prompt the user for a string in a new editor window.

    :param question: Question to ask.
    :param default: Add default value.
    :param blacklist: Retry if user input is found in 'blacklist'.
    :param instruction: A commented text that appears in the editor window to give the user instructions
    :param file_type: Specify a file type for the editor window. This can be useful for syntax highligting etc.
    :param remove_comments: Lines starting with a `#` will be removed from the user's input text.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    """
    return _string_base(
        question=question,
        default=default,
        blacklist=blacklist,
        open_editor=True,
        editor_instruction=instruction,
        editor_file_type=file_type,
        editor_remove_comments=remove_comments,
        fmt=fmt,
        fmt_question=fmt_question,
        fmt_default=fmt_default,
        fmt_prompt=fmt_prompt,
    )


def string(
    question: str,
    default: Optional[str] = None,
    blacklist: Optional[list] = None,
    multiline: bool = False,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> str:
    """
    Prompt the user for a string.

    :param question: Question to ask.
    :param default: Define a default value.
    :param blacklist: Retry if user input is found in 'blacklist'.
    :param multiline: Allow multiline answers. Use ctrl+d or ctrl+c to send.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    """
    return _string_base(
        question=question,
        default=default,
        blacklist=blacklist,
        open_editor=False,
        multiline=multiline,
        fmt=fmt,
        fmt_question=fmt_question,
        fmt_default=fmt_default,
        fmt_prompt=fmt_prompt,
    )


def integer(
    question: str,
    default: Optional[str] = None,
    blacklist: Optional[List[int]] = None,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> Union[int, None]:
    """
    Prompt the user for an integer.

    :param question: Question to ask.
    :param default: Add default value.
    :param blacklist: Retry if user input is found in 'blacklist'.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    """
    fmt = fmt or [None, None, None]
    fmt_question = fmt_question or fmt[0] or "\n{}\n"
    fmt_default = fmt_default or fmt[1] or "[{}]"
    fmt_prompt = fmt_prompt or fmt[2] or "> {}\n"
    fmt_prompt_start = fmt_prompt.split("{}")[0]
    fmt_prompt_end = fmt_prompt.split("{}")[1]

    if default:
        prompt = (
            fmt_question.format(question)
            + fmt_default.format(default)
            + fmt_prompt_start
        )
    else:
        prompt = fmt_question.format(question) + fmt_prompt_start

    answer: str = input(prompt) or default or ""

    print(fmt_prompt_end, end="")

    retry = False
    return_val: Union[int, None] = None

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
        print("Invalid input." + fmt_prompt_end)

        return_val = integer(
            question=question,
            default=default,
            blacklist=blacklist,
            fmt=fmt,
            fmt_question=fmt_question,
            fmt_default=fmt_default,
            fmt_prompt=fmt_prompt,
        )

    return return_val


def confirm(
    question: str,
    default: Optional[str] = None,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> bool:
    """
    Prompt the user to confirm with [y|yes] or [n|no].

    :param question: Question to ask.
    :param default: Add default value.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    """
    fmt = fmt or [None, None, None]
    fmt_question = fmt_question or fmt[0] or "\n{}\n"
    fmt_default = fmt_default or fmt[1] or "[{}]"
    fmt_prompt = fmt_prompt or fmt[2] or "> {}\n"
    fmt_prompt_start = fmt_prompt.split("{}")[0]
    fmt_prompt_end = fmt_prompt.split("{}")[1]

    if default:
        prompt = (
            fmt_question.format(question)
            + fmt_default.format(default)
            + fmt_prompt_start
        )
    else:
        prompt = fmt_question.format(question) + fmt_prompt_start

    return_val = None

    answer: str = input(prompt) or default or ""

    print(fmt_prompt_end, end="")

    if answer and answer.lower() in ["y", "yes", "true", "1"]:
        return_val = True

    elif answer and answer.lower() in ["n", "no", "false", "0"]:
        return_val = False

    else:
        return_val = confirm(
            question=question,
            default=default,
            fmt=fmt,
            fmt_question=fmt_question,
            fmt_default=fmt_default,
            fmt_prompt=fmt_prompt,
        )

    return return_val


def list_of_string(
    question: str,
    default: Optional[Union[list, str]] = None,
    blacklist: Optional[list] = None,
    fmt=["\n{}\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_default=None,
    fmt_prompt=None,
) -> list:
    """
    Prompt the user for a list of strings. Values are seperated with commas.

    :param question: Question to ask.
    :param default: Add default value.
    :param blacklist: Retry if user input is found in 'blacklist'.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    """
    fmt = fmt or [None, None, None]
    fmt_question = fmt_question or fmt[0] or "\n{}\n"
    fmt_default = fmt_default or fmt[1] or "[{}]"
    fmt_prompt = fmt_prompt or fmt[2] or "> {}\n"
    fmt_prompt_end = fmt_prompt.split("{}")[1]

    if isinstance(default, (list, tuple)):
        default = ", ".join(default)

    answer = string(
        question=question,
        default=default,
        blacklist=None,
        fmt=fmt,
        fmt_question=fmt_question,
        fmt_default=fmt_default,
        fmt_prompt=fmt_prompt,
    )

    retry = False

    return_val = [item.strip() for item in answer.split(",")]

    if blacklist:
        for item in return_val:
            if item in blacklist:
                retry = True

    if retry:
        print("Invalid input." + fmt_prompt_end)

        return_val = list_of_string(
            question=question,
            default=default,
            blacklist=blacklist,
            fmt=fmt,
            fmt_question=fmt_question,
            fmt_default=fmt_default,
            fmt_prompt=fmt_prompt,
        )

    return return_val


def select(
    question: str,
    options: Union[dict, list, tuple],
    default: Optional[Union[str, int]] = None,
    custom_key: Optional[Union[str, int]] = None,
    fmt=["\n{}\n", "  {}: {}", "\n", "[{}]", "> {}\n"],
    fmt_question=None,
    fmt_option=None,
    fmt_options_end=None,
    fmt_default=None,
    fmt_prompt=None,
    fmt_custom=["\n{}\n", "[{}]", "> {}\n"],
    fmt_custom_question=None,
    fmt_custom_default=None,
    fmt_custom_propmt=None,
) -> Tuple[Union[int, str], Any]:
    """
    Prompt the user to select an option from a list of options.

    :param question: Question to ask.
    :param options: The options which the user can choose from.
    :param default: Add default value.
    :param custom_key: If the user selects this key, s/he can type in a custom value.
    :param fmt_question: Define a template for displaying the question.
    :param fmt_option: Define a template for displaying the each option.
    :param fmt_options_end: Use this to display something behind the option list.
    :param fmt_default: Define a template for displaying the default value.
    :param fmt_prompt: Define a template for displaying the prompt line.
    :param fmt_custom_question: Define a template for displaying the question of the custom string input.
    :param fmt_custom_default: Define a template for displaying the default value of the custom string input.
    :param fmt_custom_prompt: Define a template for displaying the prompt line of the custom string input.
    """
    fmt = fmt or [None, None, None, None, None]
    fmt_question = fmt_question or fmt[0] or "\n{}\n"
    fmt_option = fmt_option or fmt[1] or "  {}: {}"
    fmt_options_end = fmt_options_end or fmt[2] or "\n"
    fmt_default = fmt_default or fmt[3] or "[{}]"
    fmt_prompt = fmt_prompt or fmt[4] or "> {}\n"
    fmt_prompt_start = fmt_prompt.split("{}")[0]
    fmt_prompt_end = fmt_prompt.split("{}")[1]

    fmt_custom = fmt_custom or [None, None, None]
    fmt_custom_question = fmt_custom_question or fmt_custom[0] or "\n{}\n"
    fmt_custom_default = fmt_custom_default or fmt_custom[1] or "[{}]"
    fmt_custom_propmt = fmt_custom_propmt or fmt_custom[2] or "> {}\n"

    if default:
        prompt = fmt_options_end + fmt_default.format(default) + fmt_prompt_start
    else:
        prompt = fmt_options_end + fmt_prompt_start

    print(fmt_question.format(question))

    # Print Options

    if isinstance(options, (list, tuple)):
        for key, option in enumerate(options):
            print(fmt_option.format(key, str(option)))

    elif isinstance(options, dict):
        for key, option in options.items():
            print("  {}: {}".format(key, str(option)))

    # Let User Choose Option

    selected_key: Union[int, str] = input(prompt) or str(default)

    # Validate Input
    retry = True
    selected_value = ""

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
        selected_value = string(
            selected_value,
            fmt_question=fmt_custom_question,
            fmt_default=fmt_custom_default,
            fmt_prompt=fmt_custom_propmt,
        )

    # If Input Invalid, recurse.
    print(fmt_prompt_end, end="")

    if retry:
        selected_key, selected_value = select(
            question=question,
            options=options,
            default=default,
            custom_key=custom_key,
            fmt_question=fmt_question,
            fmt_option=fmt_option,
            fmt_options_end=fmt_options_end,
            fmt_default=fmt_default,
            fmt_prompt=fmt_prompt,
            fmt_custom_question=fmt_custom_question,
            fmt_custom_default=fmt_custom_default,
            fmt_custom_propmt=fmt_custom_propmt,
        )

    return selected_key, selected_value


class Prompt:
    def __init__(
        self,
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
        #
        fmt_string_from_editor_question=None,
        fmt_string_from_editor_default=None,
        fmt_string_from_editor_prompt=None,
        #
        fmt_string_question=None,
        fmt_string_default=None,
        fmt_string_prompt=None,
        #
        fmt_integer_question=None,
        fmt_integer_default=None,
        fmt_integer_prompt=None,
        #
        fmt_confirm_question=None,
        fmt_confirm_default=None,
        fmt_confirm_prompt=None,
        #
        fmt_list_of_string_question=None,
        fmt_list_of_string_default=None,
        fmt_list_of_string_prompt=None,
        #
        fmt_select_question=None,
        fmt_select_option=None,
        fmt_select_options_end=None,
        fmt_select_default=None,
        fmt_select_prompt=None,
        fmt_select_custom_question=None,
        fmt_select_custom_default=None,
        fmt_select_custom_prompt=None,
    ):
        self.fmt_question = fmt_question
        self.fmt_default = fmt_default
        self.fmt_prompt = fmt_prompt

        self.fmt_string_from_editor_question = fmt_string_from_editor_question
        self.fmt_string_from_editor_default = fmt_string_from_editor_default
        self.fmt_string_from_editor_prompt = fmt_string_from_editor_prompt

        self.fmt_string_question = fmt_string_question
        self.fmt_string_default = fmt_string_default
        self.fmt_string_prompt = fmt_string_prompt

        self.fmt_integer_question = fmt_integer_question
        self.fmt_integer_default = fmt_integer_default
        self.fmt_integer_prompt = fmt_integer_prompt

        self.fmt_confirm_question = fmt_confirm_question
        self.fmt_confirm_default = fmt_confirm_default
        self.fmt_confirm_prompt = fmt_confirm_prompt

        self.fmt_list_of_string_question = fmt_list_of_string_question
        self.fmt_list_of_string_default = fmt_list_of_string_default
        self.fmt_list_of_string_prompt = fmt_list_of_string_prompt

        self.fmt_select_question = (fmt_select_question,)
        self.fmt_select_option = (fmt_select_option,)
        self.fmt_select_options_end = (fmt_select_options_end,)
        self.fmt_select_default = (fmt_select_default,)
        self.fmt_select_prompt = (fmt_select_prompt,)
        self.fmt_select_custom_question = (fmt_select_custom_question,)
        self.fmt_select_custom_default = fmt_select_custom_default
        self.fmt_select_custom_prompt = (fmt_select_custom_prompt,)

    def string_from_editor(
        self,
        question: str,
        default: Optional[str] = None,
        blacklist: Optional[list] = None,
        instruction: Optional[str] = None,
        file_type=None,
        remove_comments=True,
        fmt=[None, None, None],
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
    ) -> str:
        """
        Prompt the user for a string in a new editor window.

        :param question: Question to ask.
        :param default: Add default value.
        :param blacklist: Retry if user input is found in 'blacklist'.
        :param instruction: A commented text that appears in the editor window to give the user instructions
        :param file_type: Specify a file type for the editor window. This can be useful for syntax highligting etc.
        :param remove_comments: Lines starting with a `#` will be removed from the user's input text.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        """
        fmt_question = (
            fmt_question
            or fmt[0]
            or self.fmt_string_from_editor_question
            or self.fmt_question
        )  # yapf: disable
        fmt_default = (
            fmt_default
            or fmt[1]
            or self.fmt_string_from_editor_default
            or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt
            or fmt[2]
            or self.fmt_string_from_editor_prompt
            or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return string_from_editor(**args)

    def string(
        self,
        question: str,
        default: Optional[str] = None,
        blacklist: Optional[list] = None,
        fmt=[None, None, None],
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
    ) -> str:
        """
        Prompt the user for a string.

        :param question: Question to ask.
        :param default: Define a default value.
        :param blacklist: Retry if user input is found in 'blacklist'.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        """
        fmt_question = (
            fmt_question or fmt[0] or self.fmt_string_question or self.fmt_question
        )  # yapf: disable
        fmt_default = (
            fmt_default or fmt[1] or self.fmt_string_default or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt or fmt[2] or self.fmt_string_prompt or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return string(**args)

    def integer(
        self,
        question: str,
        default: Optional[str] = None,
        blacklist: Optional[List[int]] = None,
        fmt=[None, None, None],
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
    ) -> Union[int, None]:
        """
        Prompt the user for an integer.

        :param question: Question to ask.
        :param default: Add default value.
        :param blacklist: Retry if user input is found in 'blacklist'.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        """
        fmt_question = (
            fmt_question or fmt[0] or self.fmt_integer_question or self.fmt_question
        )  # yapf: disable
        fmt_default = (
            fmt_default or fmt[1] or self.fmt_integer_default or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt or fmt[2] or self.fmt_integer_prompt or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return integer(**args)

    def confirm(
        self,
        question: str,
        default: Optional[str] = None,
        fmt=[None, None, None],
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
    ) -> bool:
        """
        Prompt the user to confirm with [y|yes] or [n|no].

        :param question: Question to ask.
        :param default: Add default value.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        """
        fmt_question = (
            fmt_question or fmt[0] or self.fmt_confirm_question or self.fmt_question
        )  # yapf: disable
        fmt_default = (
            fmt_default or fmt[1] or self.fmt_confirm_default or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt or fmt[2] or self.fmt_confirm_prompt or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return confirm(**args)

    def list_of_string(
        self,
        question: str,
        default: Optional[Union[list, str]] = None,
        blacklist: Optional[list] = None,
        fmt=[None, None, None],
        fmt_question=None,
        fmt_default=None,
        fmt_prompt=None,
    ) -> list:
        """
        Prompt the user for a list of strings. Values are seperated with commas.

        :param question: Question to ask.
        :param default: Add default value.
        :param blacklist: Retry if user input is found in 'blacklist'.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        """
        fmt_question = (
            fmt_question
            or fmt[0]
            or self.fmt_list_of_string_question
            or self.fmt_question
        )  # yapf: disable
        fmt_default = (
            fmt_default or fmt[1] or self.fmt_list_of_string_default or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt or fmt[2] or self.fmt_list_of_string_prompt or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return list_of_string(**args)

    def select(
        self,
        question: str,
        options: Union[dict, list, tuple],
        default: Optional[str] = None,
        custom_key: Optional[Union[str, int]] = None,
        fmt=[None, None, None, None, None],
        fmt_question=None,
        fmt_option=None,
        fmt_options_end=None,
        fmt_default=None,
        fmt_prompt=None,
        fmt_custom=[None, None, None],
        fmt_custom_question=None,
        fmt_custom_default=None,
        fmt_custom_prompt=None,
    ) -> Tuple[Union[int, str], Any]:
        """
        Prompt the user to select an option from a list of options.

        :param question: Question to ask.
        :param options: The options which the user can choose from.
        :param default: Add default value.
        :param custom_key: If the user selects this key, s/he can type in a custom value.
        :param fmt_question: Define a template for displaying the question.
        :param fmt_option: Define a template for displaying the each option.
        :param fmt_options_end: Use this to display something behind the option list.
        :param fmt_default: Define a template for displaying the default value.
        :param fmt_prompt: Define a template for displaying the prompt line.
        :param fmt_custom_question: Define a template for displaying the question of the custom string input.
        :param fmt_custom_default: Define a template for displaying the default value of the custom string input.
        :param fmt_custom_prompt: Define a template for displaying the prompt line of the custom string input.
        """
        fmt_question = (
            fmt_question or fmt[0] or self.fmt_select_question or self.fmt_question
        )  # yapf: disable
        fmt_option = fmt_option or fmt[1] or self.fmt_select_option  # yapf: disable
        fmt_options_end = (
            fmt_options_end or fmt[2] or self.fmt_select_options_end
        )  # yapf: disable
        fmt_default = (
            fmt_default or fmt[3] or self.fmt_select_default or self.fmt_default
        )  # yapf: disable
        fmt_prompt = (
            fmt_prompt or fmt[4] or self.fmt_select_prompt or self.fmt_prompt
        )  # yapf: disable

        fmt_custom_question = (
            fmt_custom_question
            or fmt_custom[0]
            or self.fmt_select_custom_question
            or self.fmt_question
        )  # yapf: disable
        fmt_custom_default = (
            fmt_custom_default
            or fmt_custom[1]
            or self.fmt_select_custom_default
            or self.fmt_default
        )  # yapf: disable
        fmt_custom_prompt = (
            fmt_custom_prompt
            or fmt_custom[2]
            or self.fmt_select_custom_prompt
            or self.fmt_prompt
        )  # yapf: disable

        args = locals()
        del args["self"]
        del args["fmt"]

        return select(**args)
