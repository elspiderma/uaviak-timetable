import json
from vk_bot.keyboard.buttons.button import Button


class ButtonText(Button):
    BLUE = 'primary'
    WHITE = 'secondary'
    RED = 'negative'
    GREEN = 'positive'

    def __init__(self, label: str, color: str = None, payload: dict = None):
        super().__init__('text', color)
        self.label = label
        self.payload = payload
        self.color = color

    def to_dict(self):
        dict_json = super().to_dict()

        dict_json['action']['label'] = self.label
        dict_json['action']['payload'] = json.dumps(self.payload) if self.payload else None
        dict_json['color'] = self.color

        return dict_json
