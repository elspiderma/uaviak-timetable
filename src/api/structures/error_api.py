from structures import JsonStructure


class ErrorApi(JsonStructure):
    def __init__(self, message: str):
        self.message = message
