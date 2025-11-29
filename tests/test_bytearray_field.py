import pytest

from packetutil import BytearrayField

@pytest.fixture
def basic_field():
    f = BytearrayField(3)
    return f

def test_len(basic_field):
    assert len(basic_field) == 3


def test_pack_bad_arguments(basic_field):
    # Not a bytes-like
    with pytest.raises(TypeError):
        basic_field.pack("not a bytes-like")

    # Wrong length
    with pytest.raises(ValueError):
        basic_field.pack(bytearray(4))


def test_unpack_bad_arguments(basic_field):
    # Not a bytes-like
    with pytest.raises(TypeError):
        basic_field.unpack("not a bytes-like")

    # Wrong length
    with pytest.raises(ValueError):
        basic_field.unpack(bytearray(4))


def test_pack(basic_field):
    to_pack = bytearray([1, 2, 3])
    assert basic_field.pack(to_pack) == to_pack


def test_unpack(basic_field):
    to_unpack = bytearray([1, 2, 3])
    assert basic_field.unpack(to_unpack) == to_unpack
