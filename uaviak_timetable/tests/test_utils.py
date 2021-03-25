from uaviak_timetable.utils import is_string_one_unique_char


def test_is_string_one_unique_char():
    assert not is_string_one_unique_char('aksdlkrebebrebbebr', 'a')
    assert not is_string_one_unique_char('1' * 100, '7')

    assert is_string_one_unique_char('a' * 100, 'a')
    assert is_string_one_unique_char('-' * 100, '-')
