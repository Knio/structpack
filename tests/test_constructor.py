import structpack
import pytest

class TestMsg(structpack.msg):
    a = structpack.int
    b = structpack.value



def test_constructor():
    t1 = TestMsg(1, "Test")
    assert t1.a == 1
    assert t1.b == "Test"
    assert t1.pack() == (1, "Test")

    t1 = TestMsg(a=1, b="Test")
    assert t1.a == 1
    assert t1.b == "Test"
    assert t1.pack() == (1, "Test")

    with pytest.raises(ValueError):
        # cannot mix args
        t1 = TestMsg(1, b="Test")

    with pytest.raises(KeyError):
        # all args are required
        t1 = TestMsg(a=1)
