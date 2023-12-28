from block_types.DataBlock import DataBlock


class OT_1180AI(DataBlock):
    """Appears in Touch&Travel tickets.
    Field names have been inferred from the RCT2 output."""

    fields = [
        ("customer?", 7),
        ("vorgangs_num", 8),
        ("unknown1", 5),
        ("unknown2", 2),
        ("full_name", 20),
        ("adults#", 2, int),
        ("children#", 2, int),
        ("unknown3", 2),
        ("description", 20),
        ("ausweis?", 10),
        ("unknown4", 7),
        ("valid_from", 8),
        ("valid_to?", 8),
        ("unknown5", 5),
        ("start_bf", 20),
        ("unknown6", 5),
        ("ziel_bf?", 20),
        ("travel_class", 1, int),
        ("unknown7", 6),
        ("unknown8", 1),
        ("issue_date", 8),
    ]
