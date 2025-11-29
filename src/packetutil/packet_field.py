from abc import ABC, abstractmethod
from collections import namedtuple
import struct

class PacketField(ABC):
    """Base class for packet fields."""

    FieldSpec = namedtuple('FieldSpec', ['type_spec', 'size'])
    _signed_types = {
        'int8': FieldSpec('b', 1),
        'int16': FieldSpec('h', 2),
        'int32': FieldSpec('i', 4),
        'int64': FieldSpec('q', 8),
        'float': FieldSpec('f', 4),
        'double': FieldSpec('d', 8)
    }
    _unsigned_types = {
        'uint8': FieldSpec('B', 1),
        'uint16': FieldSpec('H', 2),
        'uint32': FieldSpec('I', 4),
        'uint64': FieldSpec('Q', 8)
    }
    _field_types = {
        **_signed_types,
        **_unsigned_types
    }

    @abstractmethod
    def pack(self, value):
        """Convert the field from python type to bytes-like."""
        pass

    @abstractmethod
    def unpack(self, value):
        """Convert the field from bytes-like to python type."""
        pass

    @abstractmethod
    def __len__(self):
        """Return the length the packed field in bytes."""

