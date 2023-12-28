from block_types.DataBlock import DataBlock

from block_types.utils import german_date_parser, date_parser


class OT_0080BL(DataBlock):
    def read_sblocks(self, res):
        def passagier_parser(x):
            x = [int(i) for i in x.split("-")]
            return {
                "Erwachsene": x[0],
                "Bahncards": x[1],
                "Bahncard": {
                    0: 0,
                    19: 50,
                    78: 50,
                    49: 25,
                    27: "Einsteiger BahnCard 25 (Abo frei)",
                    39: "Einsteiger BahnCard 25 (mit Abo)",
                }[int(x[2])],
            }

        ident = lambda x: x

        typen = {
            "001": ("Preismodell", ident),
            "002": ("Produktklasse Gesamtticket", {"0": "C", "1": "B", "2": "A"}),
            "003": ("Produktklasse Hinfahrt", ident),
            "004": ("Produktklasse Rückfahrt", ident),
            "009": ("Passagiere", passagier_parser),
            "012": ("Kinder", int),
            "014": ("Klasse", lambda x: int(x[-1])),
            "015": ("H-Start-Bf", ident),
            "016": ("H-Ziel-Bf", ident),
            "017": ("R-Start-Bf", ident),
            "018": ("R-Ziel-Bf", ident),
            "019": ("Vorgangsnr./Flugscheinnr.", ident),
            "020": ("Vertragspartner", ident),
            "021": ("VIA", ident),
            "023": ("Personenname", ident),
            "026": (
                "Preisart",
                {"12": "Normalpreis", "13": "Sparpreis", "3": "Rail&Fly"},
            ),
            "027": ("CC-#/Ausweis-ID", ident),
            "028": ("Vorname, Name", lambda x: x.split("#")),
            "031": ("Gültig von", german_date_parser),
            "032": ("Gültig bis", german_date_parser),
            "035": ("Start-Bf-ID", int),
            "036": ("Ziel-Bf-ID", int),
            "040": ("Anzahl Personen", int),
            "041": ("TBD EFS Anzahl", int),
        }

        ret = {}

        for i in range(res["data_count"]):
            assert self.read(1) == b"S"
            typ = self.read(3)
            l = int(self.read(4))
            dat = self.read(l)

            typ, mod = typen.get(typ, (typ, ident))
            dat = mod.get(dat, dat) if type(mod) == dict else mod(dat)

            ret[typ] = dat
        return ret

    def read_auftraege(self, res):
        version_2_fields = [
            ("certificate", 11),
            ("padding", 11),
            ("valid_from", 8, date_parser),
            ("valid_to", 8, date_parser),
            ("serial", 8, lambda x: int(x.split(b"\x00")[0])),
        ]
        # V3: 10102017 10102017 265377293\x00 12102017 12102017 265377294\x00
        version_3_fields = [
            ("valid_from", 8, date_parser),
            ("valid_to", 8, date_parser),
            ("serial", 10, lambda x: int(x.split(b"\x00")[0])),
        ]
        fields = version_2_fields if self.header["version"] < 3 else version_3_fields
        return [self.dict_read(fields) for i in range(res["auftrag_count"])]

    fields = [
        ("TBD0", 2),
        # '00' bei Schönem WE-Ticket / Ländertickets / Quer-Durchs-Land
        # '00' bei Vorläufiger BC
        # '02' bei Normalpreis Produktklasse C/B, aber auch Ausnahmen
        # '03' bei normalem IC/EC/ICE Ticket
        # '04' Hinfahrt A, Rückfahrt B; Rail&Fly ABC; Veranstaltungsticket; auch Ausnahmen
        # '05' bei Facebook-Ticket, BC+Sparpreis+neue BC25 (Ticket von 2011)
        # '18' bei Kauf via Android App
        ("auftrag_count", 1, int),
        ("blocks", 0, None, read_auftraege),
        ("data_count", 2, int),
        ("data", 0, None, read_sblocks),
    ]
