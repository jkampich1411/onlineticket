from block_types.DataBlock import DataBlock


class OT_U_TLAY(DataBlock):
    CSI = "\x1b["  # Escape sequence

    def read_fields(self, res):
        fields = [
            ("line", 2, int),
            ("column", 2, int),
            ("height", 2, int),
            ("width", 2, int),
            (
                "formating",
                1,
                {
                    b"0": "default",
                    b"1": "bold",
                    b"2": "italic",
                    b"3": "bold & italic",
                    b"4": 'small font (the "132-font" in RCT-2)',
                    b"5": "small + bold",
                    b"6": "small + italic",
                    b"7": "small + bold + italic",
                },
            ),
            ("text_length", 4, int),
            ("text", lambda self, res: res["text_length"], lambda x: x.decode()),
        ]
        ret = []
        for i in range(res["field_count"]):
            ret.append(self.dict_read(fields))

        return ret

    def __str__(self):
        """Actually render the TLAY."""
        fields = self.data["fields"]
        fields.sort(key=lambda f: f.get("line", 0) * 100 + f.get("column", 0))
        line = -1
        res = []
        for field in fields:
            new_line = field.get("line", line)
            if new_line > line:
                res.append("\n" * (new_line - line))
                line = new_line
            if "column" in field:
                res.append(self.CSI + "%dG" % (field["column"]))
            formating = field.get("formating", "")
            if "bold" in formating:
                res.append(self.CSI + "1m")
            if "small" in formating:
                res.append(self.CSI + "2m")
            if "italic" in formating:
                res.append(self.CSI + "3m")
            res.append(field.get("text", ""))
            res.append(self.CSI + "m")

        return "OT_U_TLAY (len: %d, version: %d, fields: %d)" % (
            self.header["length"],
            self.header["version"],
            len(fields),
        ) + "".join(res)

    def __repr__(self):
        return super(OT_U_TLAY, self).__repr__()

    fields = [
        ("standard", 4),
        ("field_count", 4, int),
        ("fields", 0, None, read_fields),
    ]
