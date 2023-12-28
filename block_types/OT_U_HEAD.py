from block_types.DataBlock import DataBlock

from block_types.utils import datetime_parser


class OT_U_HEAD(DataBlock):
    fields = [
        ("carrier", 4),
        ("auftragsnummer", 8),
        ("padding", 12),
        ("creation_date", 12, datetime_parser),
        (
            "flags",
            1,
            lambda x: ",".join(
                ["international"]
                if int(x) & 1
                else [] + ["edited"]
                if int(x) & 2
                else [] + ["specimen"]
                if int(x) & 4
                else []
            ),
        ),
        ("language", 2),
        ("language_2", 2),
    ]
