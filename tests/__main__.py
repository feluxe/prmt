import prmt


def test_string():

    s = prmt.string(question='Enter string: (simple)')
    s = prmt.string(question='Enter string: (simple)')

    s = prmt.string(
        question='Enter string (Default):',
        default='Joe',
    )
    s = prmt.string(
        question='Enter string: (Default)',
        default='Joe',
    )

    s = prmt.string(
        question='Enter string (Short)',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    s = prmt.string(
        question='Enter string (Short; Default)',
        default='James',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    s = prmt.string(
        question='Enter string (Short; No empty)',
        fmt=['{} ', '[{}] ', '> {}'],
        blacklist=[''],
    )

    s = prmt.string(
        question='Enter string (Short; Default; In editor)',
        default='hello',
        fmt=['{} ', '[{}] ', '> {}'],
        open_editor=True,
    )

    s = prmt.string(
        question='Enter string (In editor)',
        open_editor=True,
    )

    s = prmt.string(
        question='Enter string (No empty)',
        blacklist=[''],
    )


def test_confirm():

    b = prmt.confirm(question='Confirm [y|n]:')
    b = prmt.confirm(question='Confirm [y|n] (Default):', default='y')


def test_select():

    k, v = prmt.select(question='Select item ():', options=['a', 'b', 'c'])
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Default):',
        options=['a', 'Enter custom string', 'c'],
        default=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Default; Custom):',
        options=['a', 'Enter custom string', 'c'],
        default=1,
        custom_key=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Key as int; Value as str):',
        options={0: 'a', 1: 'b', 2: 'c'},
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Key as str; Value as str):',
        options={'0': 'a', '1': 'b', '2': 'c'},
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Key as str; Value as str; Default as int):',
        options={'0': 'a', '1': 'b', '2': 'c'},
        default=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Key as str; Value as str; Default as str):',
        options={'0': 'a', '1': 'b', '2': 'c'},
        default='1',
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select item (Key as word; Value as int; Default as word):',
        options={'foo': 0, 'bar': 1, 'baz': 2},
        default='bar',
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is int

    k, v = prmt.select(
        question=
        'Select item (Key as word; Value as int|str; Default as word; Custom):',
        options={'foo': 'Enter custom value', 'bar': 1, 'baz': 2},
        default='foo',
        custom_key='foo',
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str


def test_list():

    v = prmt.list_of_str(question='Enter values: (Simple)')
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_str(
        question='Enter values: (Default as str)',
        default='lol, nice',
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_str(
        question='Enter values: (Default as list)',
        default=['lol, nice'],
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_str(
        question='Enter values: (Blacklist word)',
        default=['lol, nice'],
        blacklist=['lol']
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_str(question='Enter values: (Blacklist empty)', blacklist=[''])
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_of_str(
        question='Enter values: (Short)',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.list_of_str(
        question='Enter values: (Short)',
        fmt=['{} ', '[{}] ', '> {}'],
    )


def test_integer():

    v = prmt.integer(question='Enter int: (Simple)')
    print(v)

    assert type(v) in [int, type(None)]

    v = prmt.integer(
        question='Enter int: (Short)',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.integer(
        question='Enter int: (Short)',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.integer(question='Enter int: (Blacklist None)', blacklist=[None])
    print(v)
    print()

    assert type(v) is int

    v = prmt.integer(
        question='Enter int: (Fmt None)',
        fmt=None,
    )


test_string()
test_confirm()
test_select()
test_list()
test_integer()
