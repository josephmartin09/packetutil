# packetutil

**`packetutil`** is a Python utility library for defining and manipulating custom binary packet structures using flexible field definitions. It makes it easy to pack Python dictionaries into bytearrays and unpack bytearrays back into structured data — with support for bitfields, bytearrays, and typed fields.

## Features

- Define binary packet formats with intuitive field objects
- Convert Python dictionaries to binary with `pack()`
- Decode binary into dictionaries with `unpack()`
- Supports:
  - Typed fields (`uint8`, `uint16`, etc.)
  - Fixed-size byte arrays
  - Bitfields with named subfields and bit lengths

## Installation

This package isn't on PyPI yet, but you can build and install it locally:

```bash
git clone https://github.com/yourusername/packetutil.git
cd packetutil
python3 setup.py bdist_wheel
pip install dist/packetutil-*.whl
```

## Usage
Define your packet structure
```python
from packetutil import PacketFormatter, TypeField, BytearrayField, BitField

fields = {
    'type_f': TypeField('uint16', big_endian=False),
    'byte_f': BytearrayField(4),
    'bit_f': BitField('uint16', {
        'field1': 3,
        'field2': 6,
        'field3': 7
    })
}
```

Pack data into a bytearray
```python
data = {
    'type_f': 1,
    'byte_f': bytearray(4 * [0]),
    'bit_f': {
        'field1': 7,
        'field2': 20,
        'field3': 30
    }
}

packed = formatter.pack(data)
print(packed)
# Output:
# bytearray([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEA, 0x1E])
```

Unpack a bytearray into structured data
```python
parsed = formatter.unpack(bytearray([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEA, 0x1E]))
print(parsed)
# Output:
# {
#     'type_f': 1,
#     'byte_f': bytearray([0, 0, 0, 0]),
#     'bit_f': {
#         'field1': 7,
#         'field2': 20,
#         'field3': 30
#     }
# }
```
