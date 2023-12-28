from block_types.DataBlock import DataBlock

from block_types.utils import vor_datetime_parser


class OT_3306FI(DataBlock):
    """Appears in VOR tickets."""

    fields = [
        ("valid_from", 16, vor_datetime_parser),
        ("valid_to", 16, vor_datetime_parser),
        ("unknown_content", 43),
    ]
