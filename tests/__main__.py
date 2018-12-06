import prmt


def test_string():

    s1 = prmt.string(question='Enter first name:')
    s2 = prmt.string(question='Enter last name:')

    s = prmt.string(question='Enter first name:', default='Joe')
    s = prmt.string(question='Enter last name:', default='Joe')
    # s = prmt.string(question='Enter name', default='hello', margin=(3, 3))

    s = prmt.string(
        question='Enter first name',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    s = prmt.string(
        question='Enter last name',
        default='James',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    s = prmt.string(
        question='Enter last name (force val)',
        fmt=['{} ', '[{}] ', '> {}'],
        blacklist=[''],
    )

    s = prmt.string(
        question='Enter last name (in editor)',
        default='hello',
        fmt=['{} ', '[{}] ', '> {}'],
        open_editor=True,
    )

    s = prmt.string(
        question='Enter last name (in editor)',
        default='hello',
        open_editor=True,
    )

    s = prmt.string(
        question='Enter last name (force val)',
        blacklist=[''],
    )


def test_confirm():

    b = prmt.confirm(question='Confirm [y|n]:')
    b = prmt.confirm(question='Confirm [y|n]:', default='y')


def test_select():

    k, v = prmt.select(question='Select:', options=['a', 'b', 'c'])
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select:',
        options=['a', 'Enter custom name', 'c'],
        default=1,
        custom_key=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(question='Select:', options={0: 'a', 1: 'b', 2: 'c'})
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is int
    assert type(v) is str

    k, v = prmt.select(
        question='Select:', options={'0': 'a', '1': 'b', '2': 'c'}
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select:',
        options={'0': 'a', '1': 'b', '2': 'c'},
        default=1,
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select:',
        options={'0': 'a', '1': 'b', '2': 'c'},
        default='1',
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is str

    k, v = prmt.select(
        question='Select:',
        options={'foo': 0, 'bar': 1, 'baz': 2},
        default='bar',
    )
    print(k, v)
    print(type(k), type(v))
    print()

    assert type(k) is str
    assert type(v) is int

    k, v = prmt.select(
        question='Select:',
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

    v = prmt.list_(question='Enter values:')
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_(question='Enter values:', default='lol, nice')
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_(question='Enter values:', default=['lol, nice'])
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_(
        question='Enter values:', default=['lol, nice'], blacklist=['lol']
    )
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_(question='Enter values:', blacklist=[''])
    print(v)
    print()

    assert type(v) is list

    v = prmt.list_(
        question='Enter values:',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.list_(
        question='Enter values:',
        fmt=['{} ', '[{}] ', '> {}'],
    )


def test_integer():

    v = prmt.integer(question='Enter int:')
    print(v)

    assert type(v) in [int, type(None)]

    v = prmt.integer(
        question='Enter int:',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.integer(
        question='Enter int:',
        fmt=['{} ', '[{}] ', '> {}'],
    )

    v = prmt.integer(question='Enter int:', blacklist=[None])
    print(v)
    print()

    assert type(v) is int


test_string()
test_confirm()
test_select()
test_list()
test_integer()
