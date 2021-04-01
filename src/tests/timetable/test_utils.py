import pytest

from timetable.utils import is_string_one_unique_char, ittr_string_with_index, index_upper


def test_is_string_one_unique_char():
    assert not is_string_one_unique_char('aksdlkrebebrebbebr', 'a')
    assert not is_string_one_unique_char('1' * 100, '7')

    assert is_string_one_unique_char('a' * 100, 'a')
    assert is_string_one_unique_char('-' * 100, '-')


def test_ittr_string_with_index():
    assert tuple(ittr_string_with_index('hello')) == ((0, 'h'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o'))
    assert tuple(ittr_string_with_index('world', True)) == ((4, 'd'), (3, 'l'), (2, 'r'), (1, 'o'), (0, 'w'))
    assert tuple(ittr_string_with_index('')) == ()


def test_index_upper():
    assert index_upper('Hello World') == 0
    assert index_upper('testString') == 4
    assert index_upper('HELLOworLd', True) == 8
    assert index_upper('testStringS', True) == 10

    with pytest.raises(ValueError) as e:
        index_upper('no_upper_string')

    assert str(e.value) == 'upper letter case not found'
