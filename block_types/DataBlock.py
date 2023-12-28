dict_str = lambda d: "\n" + "\n".join(
    ["%s:\t%s" % (k, str_func(v).replace("\n", "\n")) for k, v in d.items()]
)
list_str = lambda l: "\n" + "\n".join(
    ["%d:\t%s" % (i, str_func(v).replace("\n", "\n")) for i, v in enumerate(l)]
)
str_func = lambda v: {dict: dict_str, list: list_str}.get(
    type(v), str if isinstance(v, DataBlock) else repr
)(v)


class DataBlock(object):
    """
    A DataBlock with a standard-header. The base for custom implementations.
    Also provides features for easy definition of custom fields.
    """

    generic = [("head", 6), ("version", 2, int), ("length", 4, int)]
    fields = []

    def __init__(self, data, offset=0):
        self.stream = data
        self.offset = offset
        self.header = self.dict_read(self.generic)
        self.data = self.dict_read(self.fields)

    def __str__(self):
        return "%s\t%s%s" % (
            self.__class__.__name__,
            dict_str(self.header).replace("\n", "\n\t"),
            dict_str(self.data).replace("\n", "\n\t"),
        )

    def read(self, l):
        res = self.stream[self.offset : self.offset + l]
        self.offset += l
        return res

    def dict_read(self, directory):
        res = {}
        for val in directory:
            key = val[0]
            l = val[1]
            if type(l) != int:
                l = l(self, res)
            dat = self.read(l)
            if len(val) > 2 and val[2] is not None:
                if type(val[2]) == dict:
                    dat = val[2].get(dat, dat)
                else:
                    try:
                        dat = val[2](dat)
                    except Exception as e:
                        print("Couldn't decode", val, repr(dat), self.__class__)
                        print(dict_str(res))
                        raise
            res[key] = dat
            if len(val) > 3:
                dat = val[3](self, res)
            res[key] = dat
        return res
