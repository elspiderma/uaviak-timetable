from utils import Object2Json


class ErrorApi(Object2Json):
    def __init__(self, message: str):
        self.message = message
