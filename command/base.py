class CommandBase:
    def __init__(self, vk_api, event):
        self.vk = vk_api
        self.event = event

    def check(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
