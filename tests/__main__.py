import prmt
import readline


def test_string():
    s = prmt.string(question="Enter string: (simple)")
    s = prmt.string(question="Enter string: (simple)")

    s = prmt.string(
        question="Enter string (Default):",
        default="Joe",
    )
    s = prmt.string(
        question="Enter string: (Default)",
        default="Joe",
    )

    s = prmt.string(
        question="Enter string (Short)",
        fmt_question="{} ",
        fmt_prompt="> {}",
    )

    s = prmt.string(
        question="Enter string (Short; Default)",
        default="James",
        fmt_question="{} ",
        fmt_default="[{}] ",
        fmt_prompt="> {}",
    )

    s = prmt.string(
        question="Enter string (Short; No empty)",
        fmt_question="{} ",
        fmt_default="[{}] ",
        fmt_prompt="> {}",
        blacklist=[""],
    )

    s = prmt.string_from_editor(question="Enter string (In editor)")

    s = prmt.string_from_editor(
        question="Enter string (In editor; Default)",
        default="default value",
    )

    s = prmt.string_from_editor(
        question="Enter string (In editor; Default; Custom Instruction)",
        default="default value",
        instruction="Custom Instruction.",
    )

    s = prmt.string(
        question="Enter string (No empty)",
        blacklist=[""],
    )

    s = prmt.string(
        question="Enter string (multiline send with ctrl+c or ctrl+d)",
        multiline=True,
    )


def test_confirm():
    b = prmt.confirm(question="Confirm [y|n]:")
    b = prmt.confirm(question="Confirm [y|n] (Default):", default="y")


def test_select():
    k, v = prmt.select(question="Select item ():", options=["a", "b", "c"])
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Default):",
        options=["a", "Enter custom string", "c"],
        default=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Default; Custom):",
        options=["a", "Enter custom string", "c"],
        default=1,
        custom_key=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Key as int; Value as str):",
        options={0: "a", 1: "b", 2: "c"},
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Key as str; Value as str):",
        options={"0": "a", "1": "b", "2": "c"},
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Key as str; Value as str; Default as int):",
        options={"0": "a", "1": "b", "2": "c"},
        default=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Key as str; Value as str; Default as str):",
        options={"0": "a", "1": "b", "2": "c"},
        default="1",
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question="Select item (Key as word; Value as int; Default as word):",
        options={"foo": 0, "bar": 1, "baz": 2},
        default="bar",
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is int

    k, v = prmt.select(
        question="Select item (Key as word; Value as int|str; Default as word; Custom):",
        options={"foo": "Enter custom value", "bar": 1, "baz": 2},
        default="foo",
        custom_key="foo",
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str


def test_list():
    v = prmt.list_of_string(question="Enter values: (Simple)")
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_string(
        question="Enter values: (Default as str)",
        default="lol, nice",
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_string(
        question="Enter values: (Default as list)",
        default=["lol, nice"],
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_string(
        question="Enter values: (Blacklist word)",
        default=["lol, nice"],
        blacklist=["lol"],
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_string(question="Enter values: (Blacklist empty)", blacklist=[""])
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_string(
        question="Enter values: (Short)",
        fmt=["{} ", "[{}] ", "> {}"],
    )

    v = prmt.list_of_string(
        question="Enter values: (Short)",
        fmt=["{} ", "[{}] ", "> {}"],
    )


def test_integer():
    v = prmt.integer(question="Enter int: (Simple)")
    print(v)

    assert type(v) in [int, type(None)]

    v = prmt.integer(
        question="Enter int: (Short)",
        fmt=["{} ", "[{}] ", "> {}"],
    )

    v = prmt.integer(
        question="Enter int: (Short)",
        fmt=["{} ", "[{}] ", "> {}"],
    )

    v = prmt.integer(question="Enter int: (Blacklist empty)", blacklist=[])
    print(v)
    print()

    assert type(v) is int


def test_prompt_class():
    from prmt import Prompt

    prompt = Prompt(fmt_question="[A]{}[B]", fmt_string_default="[C]{}[D]]")

    s = prompt.string(question="Enter string: (simple)", default="foo")
    s = prompt.string_from_editor(question="Enter string (In editor)")
    b = prompt.confirm(question="Confirm [y|n]:")


test_string()
test_confirm()
test_select()
test_list()
test_integer()
test_prompt_class()
