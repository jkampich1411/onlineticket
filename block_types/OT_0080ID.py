from block_types.DataBlock import DataBlock


class OT_0080ID(DataBlock):
    fields = [
        (
            "ausweis_typ",
            2,
            {
                "01": "CC",
                "04": "BC",
                "07": "EC",
                "08": "Bonus.card business",
                "09": "Personalausweis",
                "10": "Reisepass",
                "11": "bahn.bonus Card",
            },
        ),
        ("ziffer_ausweis", 4),
    ]
