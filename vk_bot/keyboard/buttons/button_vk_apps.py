from vk_bot import Button


class ButtonVKApp(Button):
    def __init__(self, app_id: int, label: str, owner_id: int = None, hash: str = None):
        super().__init__('open_app')
        self.hash = hash
        self.label = label
        self.owner_id = owner_id
        self.app_id = app_id

    def to_dict(self):
        dict_json = super().to_dict()

        dict_json['action']['app_id'] = self.app_id
        dict_json['action']['owner_id'] = self.owner_id

        if self.label is not None:
            dict_json['action']['label'] = self.label

        if self.hash is not None:
            dict_json['action']['hash'] = self.hash

        return dict_json
