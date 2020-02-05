class Button:
    def __init__(self, type: str, *args, **kwargs):
        self.type = type

    def to_dict(self):
        dict_json = {'action': dict()}
        dict_json['action']['type'] = self.type
        return dict_json
