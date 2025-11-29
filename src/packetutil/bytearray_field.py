from . import PacketField

class BytearrayField(PacketField):
    """Bytearray PacketField."""

    def __init__(self, bytelen):
        self._len = bytelen

    def pack(self, value):
        """Convert the field from python type to bytes-like."""
        if not isinstance(value, (bytearray, bytes)):
            raise TypeError(f"{value} is not a bytes-like")
        if not len(value) == len(self):
            raise ValueError(f"{value} must be {len(self)} bytes long.")
        return value   

    def unpack(self, value):
        """Convert the field from bytes-like to python type."""
        if not isinstance(value, (bytearray, bytes)):
            raise TypeError(f"{value} is not a bytes-like")
        if not len(value) == len(self):
            raise ValueError(f"{value} must be {len(self)} bytes long.")
        return value

    def __len__(self):
        """Return the length the packed field in bytes."""
        return self._len
