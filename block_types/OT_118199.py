from json import loads
from datetime import datetime

from block_types.DataBlock import DataBlock

def datetime_parser(x):
    return datetime.strptime(x, "%y%m%d%H%M")

class OT_118199(DataBlock):
    """Appears in OEBB? tickets.
    Seems to be validity information"""

    json_temp = {}

    def init_read_validity(self):
        length = self.header["length"]
        
        data_bin = self.read(length)
        data = data_bin.decode("utf-8")
        
        self.json_temp = loads(data)
        return datetime_parser(self.json_temp["V"])
    
    def read_valid_to(self):
        return datetime_parser(self.json_temp["B"])
        
    
    fields = [
        ("valid_from", 0, None, lambda self, res: self.init_read_validity()),
        ("valid_to", 0, None, lambda self, res: self.read_valid_to()),
    ]