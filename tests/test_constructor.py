from structpack import msg, field
import pytest

class Msg(msg):
    a = field.int
    b = field.value


def test_constructor():
    t1 = Msg(1, "Test")
    assert t1.a == 1
    assert t1.b == "Test"
    assert t1.pack() == (1, "Test")

    t1 = Msg(a=1, b="Test")
    assert t1.a == 1
    assert t1.b == "Test"
    assert t1.pack() == (1, "Test")

    with pytest.raises(ValueError):
        # cannot mix args
        t1 = Msg(1, b="Test")

    with pytest.raises(KeyError):
        # all args are required
        t1 = Msg(a=1)
