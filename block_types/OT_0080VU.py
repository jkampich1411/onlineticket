from block_types.DataBlock import DataBlock, dict_str
from block_types.OT_0080VU_Tag import OT_0080VU_Tag

from block_types.datatypes import *
from block_types.utils import DateTimeCompact


class OT_0080VU(DataBlock):
    """Elektronischer Fahrschein (EFS) nach VDV-KA."""

    def read_tag(self, _, res):
        data = OT_0080VU_Tag(res["list_raw"]).header
        if data["tag"] == 0xDC:
            if data["length"] == 3 + 3:
                return uint24(data["data"])
            if data["length"] == 3 + 2:
                return uint16(data["data"])
        print("WARNING: Unexpected station data:")
        print(dict_str(data))
        return data

    def read_efs(self, res):
        fields = [
            ("berechtigungs_nr", 4, uint32),
            ("kvp_organisations_id", 2, uint16),
            ("produkt_nr", 2, uint16),
            ("pv_organisations_id", 2, uint16),
            ("valid_from", 4, DateTimeCompact),
            ("valid_to", 4, DateTimeCompact),
            ("preis", 3, uint24),
            ("sam_seqno", 4, uint32),
            ("list_length", 1, uint8),
            ("list_raw", lambda self, res: res["list_length"]),
            ("station_id", 0, None, self.read_tag)
            # The IBNR. 3 == Bayern-Ticket
        ]
        ret = []
        for i in range(res["efs_anzahl"]):
            ret.append(self.dict_read(fields))

        return ret

    fields = [
        ("terminal_id", 2, uint16),
        ("sam_id", 3, uint24),
        ("personen_anzahl", 1, uint8),
        ("efs_anzahl", 1, uint8),
        ("efs", 0, None, read_efs),
    ]
