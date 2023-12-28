import datetime
import struct

date_parser = lambda x: datetime.datetime.strptime(x.decode("utf-8"), "%d%m%Y")
german_date_parser = lambda x: datetime.datetime.strptime(x.decode("utf-8"), "%d.%m.%Y")
datetime_parser = lambda x: datetime.datetime.strptime(x.decode("utf-8"), "%d%m%Y%H%M")
vor_datetime_parser = lambda x: datetime.datetime.strptime(
    x.decode("utf-8"), "%d.%m.%Y %H:%M"
)


def DateTimeCompact(data):
    """Based on https://web.archive.org/web/20101206213922/http://www.kcefm.de/imperia/md/content/kcefm/kcefmvrr/2010_02_12_kompendiumvrrfa2dvdv_1_4.pdf"""
    day, time = struct.unpack(">HH", data)
    year = 1990 + (day >> 9)
    month = (day >> 5) & 0xF
    day = day & 0x1F
    hour = time >> 11
    minute = (time >> 5) & 0x3F
    second = time & 0x1F
    # Since hour may be 24 which is not accepted by datetime, we add it manually.
    return datetime.datetime(year, month, day, 0, minute, second) + datetime.timedelta(
        0, 3600 * hour
    )
