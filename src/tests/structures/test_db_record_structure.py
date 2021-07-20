from dataclasses import dataclass
from enum import Enum

from structures import DbRecordStructure


class TestEnum(Enum):
    value1 = 1
    value2 = 2


@dataclass
class TestA(DbRecordStructure):
    test: int
    test_enum: TestEnum
    test_list: list


class TestDbRecordStructure:
    def test_from_record_dict_ok(self):
        data = {'test': 1, 'test_enum': 1, 'test_list': [1, 2]}

        obj = TestA.from_record_dict(data)

        assert obj.test == data['test']
        assert obj.test_enum is TestEnum(data['test_enum'])
        assert obj.test_list == data['test_list']
