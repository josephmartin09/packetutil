import struct
from . import PacketField

class BitField(PacketField):
    
    def __init__(self, dtype, bitfields, big_endian=True):
        """Initialize the BitField.

        :param dtype: The datatype to pack and unpack the individual bitfields as.  This must be an unsigned type.
        :param bitfields: A dict of field_name to integers that maps the name of the bitfields to their bit lengths.
        .. note:: The sum of these bitfields must be equal to the bitlength of the dtype parameter.
        """
        # Verify dtype works for bitfields
        if not dtype in self._unsigned_types:
            raise ValueError(f"{dtype} is not a valid field type. Must be an unsigned type.")

        endian_key = ">" if big_endian else "<"
        self._struct_key = endian_key + self._unsigned_types[dtype].type_spec
        self._len = self._field_types[dtype].size
        self._bitlen = self._len * 8

        # Verify bitfield lengths add up to exactly the type length
        requested_bitlen = sum(bitfields.values())
        if not requested_bitlen == self._len * 8:
            raise ValueError(f"Length of bitfields input is {requested_bitlen} bits, but MUST be {self._bitlen} bits.")

        self._bitfields = bitfields

    def __len__(self):
        """Return the length of bitfield in bytes."""
        return self._len

    def __pack_pyint(self, value):
        """Pack a pyint using the struct library.

        :param value: A pyint that must be in the range of this BitFields dtype.
        :returns: A bytearray of the value in binary.
        """
        return struct.pack(self._struct_key, value)

    def pack(self, bitfield):
        """Convert a dict of bitfield values to a bytearray."""
        # First check if an int was passed.  If so, we can skip everything and just pack it
        if isinstance(bitfield, int):
            return self.__pack_pyint(bitfield)

        if not isinstance(bitfield, dict):
            raise TypeError(f"input to pack must be an int or dict. Got {type(bitfield)}")
        
        # Check missing keys.  Note the type cast to list is necessary to consider ordering when the keys are compared
        req_keys = list(self._bitfields.keys())
        provided_keys = list(bitfield.keys())
        if req_keys != provided_keys:
            raise ValueError(f"bitfield must be supplied the following keys in this order {self._bitfields.keys()}")

        # Convert dict to pyint
        final_pyint = 0
        bitcount = self._bitlen
        for name, field_val in bitfield.items():
            field_bitlen = self._bitfields[name]
            if field_val >= 2**field_bitlen:
                raise ValueError(f"Value of {field_val} is too large for a bitfield of {field_bitlen} bits.")
            final_pyint |= field_val << (bitcount - field_bitlen)
            bitcount -= field_bitlen
        
        # Pack the pyint as bytes
        return self.__pack_pyint(final_pyint)
        
    def unpack(self, value, as_pyint=False):
        """Unpack a bytes-like into a dict of bitfield values.

        :param value: A bytes-like to unpack.
        :param bool as_pyint: Return an int if True, otherwise a dict of each field.
        :returns: A pyint of the unpacked value, or a dict of field_name -> pyints for each bitfield.
        """
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(f"{value} is not a bytes or bytearray")

        if len(value) != self._len:
            raise ValueError(f"Bytes-like to unpack must be {self._len} bytes, but got {len(value)} bytes")

        # Unpack as pyint
        unpacked_pyint = struct.unpack(self._struct_key, value)[0]
        if as_pyint:
            return unpacked_pyint

        # Unpack bitfields
        bitcount = self._bitlen
        unpacked_fields = dict()
        for name, field_bitlen in self._bitfields.items():
            unpacked_fields[name] = unpacked_pyint >> (bitcount - field_bitlen)
            bitcount -= field_bitlen
            unpacked_pyint &= (2**bitcount - 1)

        return unpacked_fields
