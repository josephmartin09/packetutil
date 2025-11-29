import pytest

from packetutil import TypeField

# For these endian tests, all byte logic is actually handled by the struct libray.
# Therefore, it's sufficient to ensure that Typefield is just passing the correct endian key to struct
def test_big_endian():
    f = TypeField('uint32')
    assert f._struct_key.startswith(">")


def test_little_endian():
    f = TypeField('uint32', big_endian=False)
    assert f._struct_key.startswith("<")


def test_pack_invalid_type():
    f = TypeField('uint32')
    with pytest.raises(TypeError):
        f.pack("not an int or float")


def test_unpack_invalid_type():
    f = TypeField('uint32')
    with pytest.raises(TypeError):
        f.unpack("not a bytes-like")


def test_pack():
    # signed type
    f = TypeField('int16')
    assert f.pack(-300) ==  bytearray([0xFE, 0xD4])

    # unsigned type
    f = TypeField('uint16')
    assert f.pack(65236) == bytearray([0xFE, 0xD4])

    # float type
    f = TypeField('float')
    assert f.pack(1.234) == bytearray([0x3F, 0x9D, 0xF3, 0xB6])



def test_unpack():
    # signed type
    f = TypeField('int16')
    assert f.unpack(bytearray([0xFE, 0xD4])) == -300

    # unsigned type
    f = TypeField('uint16')
    assert f.unpack(bytearray([0xFE, 0xD4])) == 65236

    # float type
    f = TypeField('float')
    assert f.unpack(bytearray([0x3F, 0x9D, 0xF3, 0xB6])) == pytest.approx(1.234)


def test_len():
    f = TypeField('int8')
    assert len(f) == 1
    
    f = TypeField('int16')
    assert len(f) == 2
    
    f = TypeField('int32')
    assert len(f) == 4
    
    f = TypeField('int64')
    assert len(f) == 8

    f = TypeField('float')
    assert len(f) == 4

    f = TypeField('double')
    assert len(f) == 8
