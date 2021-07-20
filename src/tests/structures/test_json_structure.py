from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum

import pytest

from structures import JsonStructure


class TestEnum(Enum):
    value1 = 'test1_value'
    value2 = 'test2_value'


@dataclass
class TestB(JsonStructure):
    integer: int = 42
    _ignore: str = 'Hello World'


@dataclass
class TestA(JsonStructure):
    boolean: bool = False
    integer: int = 5
    string: str = 'test'
    enum: TestEnum = TestEnum.value1
    null: None = None
    sub_object: TestB = TestB()
    list_: list[int] = field(default_factory=lambda: [1, 2, 3])
    dict_: dict = field(default_factory=lambda: {'test': 1})
    tuple: tuple = (1, 2, 3, 4)
    date: date = date(2012, 1, 21)
    datetime: datetime = datetime(2012, 1, 21, 22, 54, 7)


@dataclass
class TestBError:
    pass


@dataclass
class TestAError(JsonStructure):
    def __init__(self):
        self.error_type = TestBError()


class TestObjectToJson:
    def test_to_json_dict_ok(self):
        obj = TestA()

        result = obj.to_json_dict()

        assert result['boolean'] == obj.boolean
        assert result['integer'] == obj.integer
        assert result['string'] == obj.string
        assert result['enum'] == obj.enum.value
        assert result['null'] is None
        assert result['sub_object']['integer'] == obj.sub_object.integer
        assert '_ignore' not in result['sub_object']
        assert result['list_'][0] == obj.list_[0]
        assert result['list_'][1] == obj.list_[1]
        assert result['dict_']['test'] == obj.dict_['test']
        assert result['tuple'] == obj.tuple
        assert result['date'] == obj.date.isoformat()
        assert result['datetime'] == obj.datetime.isoformat()

    def test_to_json_dict_error(self):
        obj = TestAError()

        with pytest.raises(TypeError):
            obj.to_json_dict()
