# flake8: noqa

# Information
from block_types.OT_U_HEAD import OT_U_HEAD
from block_types.OT_U_TLAY import OT_U_TLAY

# Generic
from block_types.GenericBlock import GenericBlock
from block_types.OT_RAWJSN import OT_RAWJSN

# DB
from block_types.OT_0080BL import OT_0080BL
from block_types.OT_0080ID import OT_0080ID
from block_types.OT_0080VU import OT_0080VU
from block_types.OT_1180AI import OT_1180AI

# OEBB
from block_types.OT_118199 import OT_118199

# VOR
from block_types.OT_3306FI import OT_3306FI
from block_types.OT_3306VD import OT_3306VD

block_types = {
    b"U_HEAD": OT_U_HEAD,
    b"U_TLAY": OT_U_TLAY,
    b"RAWJSN": OT_RAWJSN,
    b"0080BL": OT_0080BL,
    b"0080ID": OT_0080ID,
    b"0080VU": OT_0080VU,
    b"1180AI": OT_1180AI,
    b"118199": OT_118199,
    b"3306FI": OT_3306FI,
    b"3306VD": OT_3306VD,
}
