import pytest


def test_answer():
    assert 1 == 1 


# pylint: disable=missing-docstring, invalid-name
def f():
    raise SystemExit(1)
# pylint: enable=missing-docstring, invalid-name


def test_mytest():
    with pytest.raises(SystemExit):
        f()


class TestClass:
    def test_one(self):
        x = "this"
        assert 'h' in x
