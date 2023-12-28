from block_types.DataBlock import DataBlock

from block_types.utils import date_parser


class OT_3306VD(DataBlock):
    """Appears in VOR tickets.
    Seems to be customer information"""

    def parse_name(self, res):
        max_len = self.header["length"]
        used = (
            len(res["padding_1?"])
            + len(str(res["customer_id"]))
            + len(str(res["gender"]))
            + len(res["padding_2?"])
        )
        name_len = max_len - used
        name = self.read(name_len).decode()

        name = name[1:][:-1].split("||")
        return {"first": name[0], "last": name[1]}

    def advance_padding_until_data(self):
        ret = b""
        while True:
            current = self.read(1)
            if current != b" ":
                self.offset -= 1
                break
            ret += current

        return ret

    fields = [
        ("padding_1?", 0, None, lambda self, res: self.advance_padding_until_data()),
        ("customer_id", 6, int),
        ("gender", 1, lambda val: val.decode()),
        ("date_of_birth", 8, date_parser),
        ("padding_2?", 0, None, lambda self, res: self.advance_padding_until_data()),
        ("name", 0, None, lambda self, res: self.parse_name(res)),
    ]
