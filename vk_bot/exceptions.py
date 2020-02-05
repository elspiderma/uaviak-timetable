class VKBaseError(Exception):
    """Базовый класс представляющий ошибку, вернувшиеся от API"""
    def __init__(self, code, msg, request_param, text=None):
        super().__init__(msg)
        self.code = code
        self.msg = msg
        self.text = text
        self.request_param = request_param

    @classmethod
    def de_json(cls, data):
        return cls(
            code=data.get('error_code'),
            msg=data.get('error_msg'),
            request_param=data.get('request_params'),
            text=data.get('error_text')
        )
