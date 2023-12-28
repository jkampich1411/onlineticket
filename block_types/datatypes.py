uint8 = ord
uint16 = lambda x: x[1] | x[0] << 8
uint24 = lambda x: x[2] | x[1] << 8 | x[0] << 16
uint32 = lambda x: x[3] | x[2] << 8 | x[1] << 16 | x[0] << 24
