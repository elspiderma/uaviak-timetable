import json
from vk_bot import Button


class ButtonLocation(Button):
    def __init__(self, payload: dict = None):
        super().__init__('location')
        self.payload = payload

    def to_dict(self):
        dict_json = super().to_dict()

        dict_json['action']['payload'] = json.dumps(self.payload) if self.payload else None

        return dict_json
