"""BitField Tests.

At the moment these are pretty basic as they're only focused on uint16
"""
import pytest

from packetutil import BitField

@pytest.fixture
def short_field_big():
    fields = {
        'field1': 3,
        'field2': 6,
        'field3': 7
    }
    return BitField('uint16', fields)

@pytest.fixture
def short_field_little():
    fields = {
        'field1': 3,
        'field2': 6,
        'field3': 7
    }
    return BitField('uint16', fields, big_endian=False)    

def test_init():
    # Bad dtype
    with pytest.raises(ValueError):
        field = BitField("invalid_dtype", {})

    # Bitfield length not equal to type length
    incorrect_fields = {
        "first_3": 3,
        "one_too_many": 6
    }
    with pytest.raises(ValueError):
        field = BitField("uint8", incorrect_fields)

    # Valid case (constructor completion implies success of this test)
    correct_fields = {
        'first_3': 3,
        'last_5': 5
    }
    field = BitField('uint8', correct_fields)


def test_len(short_field_big):
    assert len(short_field_big) == 2


def test_pack_bad_arguments(short_field_big):
    # Pass in a string, which should trigger the invalid type logic
    with pytest.raises(TypeError):
        short_field_big.pack("A string")

    # Supply a dictionary that has missing keys
    missing_keys = {
        'field1': 3,
        'field3': 4
    }
    with pytest.raises(ValueError):
        short_field_big.pack(missing_keys)

    # Supply a dictionary that has misordered keys
    misordered_keys  = {
        'field1': 3,
        'field3': 4,
        'field2': 10
    }
    with pytest.raises(ValueError):
        short_field_big.pack(misordered_keys)


def test_pack_pyint(short_field_big, short_field_little):
    assert short_field_big.pack(0x87) == bytearray([0x00, 0x87])
    assert short_field_little.pack(0x87) == bytearray([0x87, 0x00])


def test_pack_dict(short_field_big, short_field_little):
    assert short_field_big.pack({
        'field1': 7,
        'field2': 20,
        'field3': 30
    }) == bytearray([0xEA,  0x1E])

    assert short_field_little.pack({
        'field1': 7,
        'field2': 20,
        'field3': 30
    }) == bytearray([0x1E,  0xEA])


def test_unpack_bad_arguments(short_field_big):
    # Unpack something that's not a bytes-like
    with pytest.raises(TypeError):
        short_field_big.unpack("not a bytes like")

    # Too many bytes
    with pytest.raises(ValueError):
        short_field_big.unpack(bytearray([0x00, 0x01, 0x02])) # One byte too many


def test_unpack_pyint(short_field_big, short_field_little):
    assert short_field_big.unpack(bytearray([0x00, 0x87]), as_pyint=True) == 0x87
    assert short_field_little.unpack(bytearray([0x87, 0x00]), as_pyint=True) == 0x87


def test_unpack_dict(short_field_big, short_field_little):
    expected_values = {
        'field1': 7,
        'field2': 20,
        'field3': 30
    }
    assert short_field_big.unpack(bytearray([0xEA,  0x1E])) == expected_values
    assert short_field_little.unpack(bytearray([0x1E,  0xEA])) == expected_values
