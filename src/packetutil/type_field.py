import struct

from . import PacketField

class TypeField(PacketField):
    """Class to perform packing and unpacking of exactly one packet field.
    
    This is the simplest type of PacketField, which allows packing/unpacking types with widths of powers of 2.
    """

    def __init__(self, dtype, big_endian=True):
        """Initialize the type field.

        :param str dtype: data type of field
        :param bool big_endian: treat bytes as big endian if True, otherwise treat bytes as little endian
        """
        if dtype not in self._field_types.keys():
            raise ValueError(f"{dtype} is not a valid field type.")
        endian_key = ">" if big_endian else "<"
        self._struct_key = endian_key + self._field_types[dtype].type_spec
        self._len = self._field_types[dtype].size

    def pack(self, value):
        """Convert value from python type to a bytes-like.
        
        :param int/float value: value to pack as bytes.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Value must be either a python int or float. Got {type(value)}")
        return struct.pack(self._struct_key, value)

    def unpack(self, value):
        """Convert value from bytes-like to python type.

        :param bytes-likes value: value to unpack to python type
        """
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(f"{value} is not a bytes or bytearray")
        return struct.unpack(self._struct_key, value)[0]

    def __len__(self):
        """Return the length of this PacketField, in bytes."""
        return self._len
