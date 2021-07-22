import pytest

from utils import is_string_one_unique_char, index_upper


class TestIsStringOneUniqueChar:
    def test_is_string_one_unique_char_true(self):
        assert is_string_one_unique_char('hhhhhhh', 'h') is True
        assert is_string_one_unique_char('aaaaaaaaaa', 'a') is True
        assert is_string_one_unique_char('-', '-') is True

    def test_is_string_one_unique_char_false(self):
        assert is_string_one_unique_char('hhhhhhh', 'a') is False
        assert is_string_one_unique_char('aaaaaaaaaaaaa', 'h') is False
        assert is_string_one_unique_char('-', '+') is False


class TestIndexUpper:
    def test_index_upper_ok(self):
        s = 'heLoO woRLd'

        assert index_upper(s) == 2
        assert index_upper(s, True) == 9

    def test_index_upper_fail(self):
        s = 'hello world'

        with pytest.raises(ValueError) as e:
            index_upper(s)

        with pytest.raises(ValueError) as e:
            index_upper(s, False)
