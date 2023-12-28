import re

from block_types.DataBlock import DataBlock


class OT_RAWJSN(DataBlock):
    """A data block containing raw json data."""

    def __init__(self, *args, **kwargs):
        super(OT_RAWJSN, self).__init__(*args, **kwargs)
        json_data = self.read(self.header["length"] - 12)
        import json

        try:
            self.data.update(json.loads(json_data))
        except:
            # json is likely unhappy about keys missing quotes
            # (e.g. {key: 'value'} instead of {'key': 'value'})
            import yaml

            try:
                self.data.update(yaml.load(json_data))
            except:
                # yaml is likely unhappy about missing spaces after colons
                # (e.g. {key:'value'} instead of {key: 'value'})
                try:
                    with_spaces = re.sub(
                        r'([,{][^}:]+?):([{[0-9\'"])', r"\1: \2", json_data
                    )
                    self.data.update(yaml.load(with_spaces))
                except:
                    print("Couldn't decode JSON data", repr(json_data))
                    raise
