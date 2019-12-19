class CommandBase:
    def __init__(self, vk_api):
        self.vk = vk_api

    def check(self, event):
        raise NotImplementedError

    def run(self, event):
        raise NotImplementedError
