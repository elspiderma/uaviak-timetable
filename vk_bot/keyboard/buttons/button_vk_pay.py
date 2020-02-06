from vk_bot import Button


class ButtonVKPay(Button):
    def __init__(self, hash: str):
        super().__init__('vkpay')
        self.hash = hash

    def to_dict(self):
        dict_json = super().to_dict()

        dict_json['action']['hash'] = self.hash

        return dict_json
