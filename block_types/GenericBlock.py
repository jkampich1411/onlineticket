from block_types.DataBlock import DataBlock


class GenericBlock(DataBlock):
    """A DataBlock whose content is unknown."""

    def __init__(self, *args, **kwargs):
        super(GenericBlock, self).__init__(*args, **kwargs)
        self.data["unknown_content"] = self.read(self.header["length"] - 12)
