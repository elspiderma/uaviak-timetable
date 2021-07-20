from enum import Enum
from utils import Object2Json


class TestEnum(Enum):
    value1 = 'test1_value'
    value2 = 'test2_value'


class TestB(Object2Json):
    IGNORE = ['ignore']

    def __init__(self):
        self.integer = 42
        self.ignore = 'Hello World'


class TestA(Object2Json):
    def __init__(self):
        self.integer = 5
        self.string = 'test'
        self.enum = TestEnum.value1
        self.null = None
        self.sub_object = TestB()
        self.list = ['test', 123]
        self.dict = {'a': 1, 'b': 2, 3: 5}


class TestObjectToJson:
    def test_to_json_dict(self):
        obj = TestA()

        result = obj.to_json_dict()

        assert result['integer'] == obj.integer
        assert result['string'] == obj.string
        assert result['enum'] == obj.enum.value
        assert result['null'] is None
        assert result['sub_object']['integer'] == obj.sub_object.integer
        assert 'ignore' not in result['sub_object']
        assert result['list'][0] == obj.list[0]
        assert result['list'][1] == obj.list[1]
        assert result['dict']['a'] == obj.dict['a']
        assert result['dict']['b'] == obj.dict['b']
        assert result['dict'][3] == obj.dict[3]
