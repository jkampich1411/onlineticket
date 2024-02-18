uint8 = ord
def uint16(x):
    return x[1] | x[0] << 8

def uint24(x):
    return x[2] | x[1] << 8 | x[0] << 16

def uint32(x):
    return x[3] | x[2] << 8 | x[1] << 16 | x[0] << 24
