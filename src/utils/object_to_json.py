from enum import Enum


class Object2Json:
    IGNORE: list[str] = []

    def to_json_dict(self) -> dict:
        def convert(val):
            if isinstance(val, Object2Json):
                return val.to_json_dict()
            elif isinstance(val, Enum):
                return val.value
            elif isinstance(val, list):
                return [convert(i) for i in val]
            elif isinstance(val, dict):
                return {k: convert(n) for k, n in val.items()}
            else:
                return val

        result = self.__dict__.copy()

        for i in self.IGNORE:
            if i in result:
                del result[i]

        for k, n in result.items():
            result[k] = convert(n)


        return result
