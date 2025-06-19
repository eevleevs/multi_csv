from pytest import mark

from .. import DuplicateColumnError, DuplicateKeyError, reader


def test_ok():
    assert (
        reader("""
            Key1, 1
            Key2, A

            Table 1
            C1,C2
            A,B

            Key3, 3

            Table 1
            C1,C2
            A,B

            Table 2
            C1,C2,C3
            1,2.5,3
            4,-5.
            ,
            ,,

            Table 3
            C1,C2
            1,-2.4
        """)
    ) == {
        'Key1': 1,
        'Key2': 'A',
        'Table 1': [{'C1': 'A', 'C2': 'B'}, {'C1': 'A', 'C2': 'B'}],
        'Key3': 3,
        'Table 2': [
            {'C1': 1, 'C2': 2.5, 'C3': 3},
            {'C1': 4, 'C2': -5.0, 'C3': ''},
        ],
        'Table 3': [{'C1': 1, 'C2': -2.4}],
    }


def test_lower_word():
    assert reader(
        """
            Table 1
            C1,C2
            1,2

            A-B Length, 3
        """,
        lower=True,
        word=True,
    ) == {
        'table1': [{'c1': 1, 'c2': 2}],
        'ablength': 3,
    }


def test_duplicate_key_1():
    assert reader(
        """
            table 1
            C1,C2,C3
            1,2

            Table1
            C1,C2,C3
            1,2,3
            4,5
        """,
        lower=True,
        word=True,
    ) == {
        'table1': [
            {'c1': 1, 'c2': 2, 'c3': ''},
            {'c1': 1, 'c2': 2, 'c3': 3},
            {'c1': 4, 'c2': 5, 'c3': ''},
        ]
    }


@mark.xfail(raises=DuplicateKeyError)
def test_duplicate_key_2():
    reader(
        """
            table 1
            C1,C2
            1,2

            Table1, 1
        """,
        lower=True,
        word=True,
    )


@mark.xfail(raises=DuplicateColumnError)
def test_duplicate_column():
    reader(
        """
            Table 1
            C1,c 1
            1,2
        """,
        lower=True,
        word=True,
    )
