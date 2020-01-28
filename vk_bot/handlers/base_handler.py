class BaseHandler:
    def __init__(self, func):
        self.func = func

    def check(self, obj):
        raise NotImplemented

    def exec(self, obj):
        self.func(obj)
