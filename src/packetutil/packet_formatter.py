from . import PacketField, TypeField

class PacketFormatter:
    """Class to pack and unpack multiple packet fields as a full packet."""

    def __init__(self, field_spec):
        """Initialize the format of the packet.

        :param field_spec: dict mapping field_name -> PacketField
        """
        if not isinstance(field_spec, dict):
            raise TypeError("field_spec param must be a dict.")

        # Validate the field_spec
        for name, packet_field in field_spec.items():
            if not isinstance(name, str):
                raise TypeError(f"name field must be a str.")
            if not isinstance(packet_field, PacketField):
                raise TypeError(f"packet field must be a PacketField instance.")
        self._field_spec = field_spec

        # Calculate byte length of this packet
        self._len = 0
        for name, packet_field in self._field_spec.items():
            self._len += len(packet_field)

    def __len__(self):
        """Return the byte length of the PacketFormatter."""
        return self._len

    def pack(self, packet_dict):
        """Convert packet_dict into a bytes-like.
        
        :param dict packet_dict: a dict mapping field_name -> desired value for this packet.  These fields must match the field_spec passed
        in the constructor.
        """
        if not isinstance(packet_dict, dict):
            raise TypeError("packet_dict must be of type dict.")

        # Check if the keys in self._field_spec are all present in this packet.  I think it's ok to allow packet_dict
        # to have extra keys not in field_spec.
        fs_keys = list(self._field_spec.keys())
        pd_keys = list(packet_dict.keys())
        if fs_keys != pd_keys:
            raise ValueError(f"packet_dict must exactly match the following keys {fs_keys}")

        # Pack the packet
        result = bytearray()
        for name, packet_value in packet_dict.items():
            result += self._field_spec[name].pack(packet_value)
        return result

    def unpack(self, packet):
        """Convert bytes-like packet to dict of field_name->python-type value.

        :param bytes-like packet: packet to convert
        """
        if not isinstance(packet, (bytes, bytearray)):
            raise TypeError("packet must be a bytes-like.")

        # For exception-tracing/general sanity, checking the length here is a good idea.
        if not len(packet) == len(self):
            raise ValueError(f"packet has byte-length {len(packet)}, but this formatter expected a byte-length of {len(self)}.")

        # Attempt to convert raw packet into dict form.
        temp_packet = packet
        result = dict()
        for name, packet_field in self._field_spec.items():
            field_byte_len = len(packet_field)
            result[name] = packet_field.unpack(temp_packet[0:field_byte_len])
            temp_packet = temp_packet[field_byte_len:]
        return result
