from block_types.DataBlock import DataBlock

from block_types.datatypes import uint8, uint16


class OT_0080VU_Tag(DataBlock):
    generic = [
        ("tag", 1, uint8),  # 0xdc
        # This may be ASN.1 TLV structure in which case additional
        # length parsing for long fields may be required some day.
        ("length", 1, uint8),
        ("type", 1, uint8),
        ("org_id", 2, uint16),
        ("data", lambda self, res: res["length"] - 3),
    ]
