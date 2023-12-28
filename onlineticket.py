#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Parser für Online-Tickets der Deutschen Bahn nach ETF-918.3
# Copyright by Hagen Fritsch, 2009-2017
# Copyright by onlineticket maintainers, 2017-2023
# Copyright by Jakob Kampichler, 2023-

import csv
import os
import zlib
import sys

from block_types import *
from block_types.DataBlock import DataBlock

try:  # pip install pycryptodome
    from Crypto.Hash import SHA1
    from Crypto.PublicKey import DSA
    from Crypto.Signature import DSS
    from Crypto.Math.Numbers import Integer
except:
    try:
        from Crypto.Hash import SHA

        print(
            "Please remove the deprecated python3-crypto package and install python3-pycryptodome instead.",
            file=sys.stderr,
        )
        exit(1)
    except:
        print(
            "Note: signature verification is disabled due to missing pycryptodome package.",
            file=sys.stderr,
        )
    SHA1, DSA, DSS, Integer = None, None, None, None

try:  # pip install pyasn1
    import pyasn1.codec.der.decoder as asn1
except:
    print(
        "Note: signature verification is disabled due to missing pyasn1 package.",
        file=sys.stderr,
    )
    asn1 = None

# Core datatypes:
DEBUG = 0


def debug(tag, arg, *extra):
    if DEBUG:
        print(tag, arg, *extra, "\n")
    return arg


class SignatureVerificationError(Exception):
    pass


def get_pubkey(issuer, keyid):
    if get_pubkey.certs is None:
        certs_filename = os.path.join(os.path.dirname(__file__), "certs.csv")
        if not os.path.exists(certs_filename):
            raise SignatureVerificationError(
                f"certificate store not found: {certs_filename}\n"
                "Use download_keys.py to create it."
            )
        get_pubkey.certs = {}
        with open(certs_filename) as certsfile:
            certreader = csv.reader(certsfile, delimiter="\t")
            for cert_issuer, xid, pubkey in certreader:
                get_pubkey.certs[(int(cert_issuer), int(xid))] = pubkey
    try:
        return get_pubkey.certs[(int(issuer), int(keyid))]
    except KeyError:
        raise SignatureVerificationError(
            f"Public key not found (issuer={issuer}, keyid={keyid})"
        )


get_pubkey.certs = None


def verifysig(message, signature, pubkey):
    if DSS is None or asn1 is None:  # pycryptodome package is missing
        raise SignatureVerificationError("Signature verification disabled")
    if not signature:
        raise SignatureVerificationError("Signature asn1 parsing error.")

    r, s = signature

    rbytes = Integer(r).to_bytes()
    sbytes = Integer(s).to_bytes()

    verifykey = DSA.import_key(pubkey)
    h = SHA1.new(message)
    verifier = DSS.new(verifykey, "fips-186-3")

    try:
        verifier.verify(h, rbytes + sbytes)
        return True
    except ValueError as e:
        raise SignatureVerificationError("Signature NOT valid: " + str(e))


class OT(DataBlock):
    def get_version(self):
        return int(self.stream[3:5].decode())

    def signature_decode(self, res):
        """Parses the asn1 signature and extracts the (r,s) tuple."""

        print(self.get_version())

        if not asn1:
            return None
        if self.get_version() == 1:
            decoded = asn1.decode(self.read(50))[0]
        elif self.get_version() == 2:
            decoded = asn1.decode(self.read(64))[0]

        return (int(decoded[0]), int(decoded[1]))

    def signature_validity(self, res):
        if len(self.stream) - self.offset - res["data_length"] > 0:
            return "INVALID (trailing data)"
        if len(self.stream) - self.offset - res["data_length"] < 0:
            return "INVALID (incomplete ticket data)"

        try:
            pubkey = get_pubkey(issuer=res["carrier"], keyid=res["key_id"])
            result = verifysig(self.stream[self.offset :], res["signature"], pubkey)
        except SignatureVerificationError as e:
            return str(e)

        return "VALID" if result else "INVALID"

    generic = [
        ("header", 3),
        ("version", 2),
        ("carrier", 4),
        ("key_id", 5),
        ("signature", 0, None, signature_decode),
        ("data_length", 4, int),
        ("signature_validity", 0, None, signature_validity),
    ]

    fields = [
        (
            "ticket",
            0,
            None,
            lambda self, res: read_blocks(
                zlib.decompress(self.read(self.header["data_length"])), read_block
            ),
        ),
    ]


def read_block(data, offset):
    block_types = {
        b"U_HEAD": OT_U_HEAD,
        b"U_TLAY": OT_U_TLAY,
        b"RAWJSN": OT_RAWJSN,
        b"0080BL": OT_0080BL,
        b"0080ID": OT_0080ID,
        b"0080VU": OT_0080VU,
        b"1180AI": OT_1180AI,
        b"3306FI": OT_3306FI,
        b"3306VD": OT_3306VD,
    }
    block_type = debug("block_type", data[offset : offset + 6], repr(data[offset:]))
    return block_types.get(block_type, GenericBlock)(data, offset)


readot = lambda x: "".join([chr(int(i, 16)) for i in x.strip().split(" ")])


def read_blocks(data, read_func):
    offset = 0
    ret = []
    while offset < len(data):
        block = read_func(data, offset)
        offset = block.offset
        ret.append(block)
    return ret


def fix_zxing(data):
    """
    ZXing parser seems to return utf-8 encoded binary data.
    See also http://code.google.com/p/zxing/issues/detail?id=1260#c4
    """
    data = data.decode("utf-8").encode("latin1")
    # zxing parsing also adds a newline to the end of the file. remove that.
    if data.endswith(b"\n"):
        data = data[:-1]
    return data


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: %s [ticket_files]" % sys.argv[0])
    ots = {}
    for ticket in sys.argv[1:]:
        try:
            tickets = [readot(i) for i in open(ticket)]
        except:
            content = open(ticket, "rb").read()
            tickets = [content]
        for binary_ticket in tickets:
            try:
                ot = OT(binary_ticket)
            except Exception as e:
                try:
                    fixed = fix_zxing(binary_ticket)
                    ot = OT(fixed)
                except Exception as f:
                    sys.stderr.write(
                        "ORIGINAL: %s\nZXING: %s\n%s: Error: %s (orig); %s (zxing)\n"
                        % (repr(ot), repr(fixed), ticket, e, f)
                    )
                    raise
            print(ot)
            ots.setdefault(ticket, []).append(ot)

    # Some more sample functionality:
    # 1. Sort by date
    # tickets = reduce(list.__add__, ots.values())
    # tickets.sort(lambda a, b: cmp(a.data['ticket'][0].data['creation_date'], b.data['ticket'][0].data['creation_date']))
    # print(list_str(tickets))
