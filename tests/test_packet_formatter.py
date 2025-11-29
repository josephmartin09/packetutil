import pytest

from packetutil import PacketFormatter
from packetutil import BitField, BytearrayField, TypeField

@pytest.fixture
def simple_fmt():
    fields = {
        'field1': TypeField('uint8'),
        'field2': TypeField('uint32')
    }
    return PacketFormatter(fields)


@pytest.fixture
def complex_fmt():
    fields = {
        'type_f': TypeField('uint16', big_endian=False),
        'byte_f': BytearrayField(4),
        'bit_f': BitField('uint16', 
            {
                'field1': 3,
                'field2': 6,
                'field3': 7
            })
    }
    return PacketFormatter(fields)


def test_invalid_field_spec():
    # Field spec not a dict
    with pytest.raises(TypeError):
        PacketFormatter("not a dict")

    # Only string keys
    with pytest.raises(TypeError):
        PacketFormatter({3: TypeField('uint8')})

    # Only PacketField Values
    with pytest.raises(TypeError):
        PacketFormatter({'field1': "not a PacketField"})

def test_len(simple_fmt, complex_fmt):
    assert len(simple_fmt) == 5
    assert len(complex_fmt) == 8


def test_pack_bad_arguments(simple_fmt):
    # argument not a dict
    with pytest.raises(TypeError):
        simple_fmt.pack("not a dict")

    # keys don't match field spec
    with pytest.raises(ValueError):
        simple_fmt.pack({"field2": 1, "field1": 3})

def test_unpack_bad_arguments(simple_fmt):
    # argument not a bytes-like
    with pytest.raises(TypeError):
        simple_fmt.unpack("not a bytes like")

    # bytearray is incorrect length for formatter
    with pytest.raises(ValueError):
        simple_fmt.unpack(bytearray(6))


def test_pack(simple_fmt, complex_fmt):
    # I hand-calculated these bytearrays
    correct_simple_res = bytearray([
        0x01, 0x01, 0x02, 0x03, 0x04
    ])

    assert simple_fmt.pack({
        'field1': 1,
        'field2': 0x01020304
    }) == correct_simple_res

    correct_complex_res = bytearray([
        0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEA,  0x1E
    ])

    assert complex_fmt.pack({
        'type_f': 1,
        'byte_f': bytearray(4*[0]),
        'bit_f': {
            'field1': 7,
            'field2': 20,
            'field3': 30
        }
    }) == correct_complex_res


def test_unpack(simple_fmt, complex_fmt):

    correct_simple_res = {
        'field1': 1,
        'field2': 0x01020304
    }

    correct_complex_res = {
        'type_f': 1,
        'byte_f': bytearray(4*[0]),
        'bit_f': {
            'field1': 7,
            'field2': 20,
            'field3': 30
        }
    }

    assert simple_fmt.unpack(bytearray([0x01, 0x01, 0x02, 0x03, 0x04])) == correct_simple_res
    assert complex_fmt.unpack(bytearray([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEA,  0x1E])) == correct_complex_res
