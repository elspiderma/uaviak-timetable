from typing import Union

import pytest

from config import Configuration, AbstractReader, TypesValue, NotFoundOption


class TestConfiguration:
    class Reader(AbstractReader):
        def __init__(self):
            self.config = {}

        def get(self, section: str, option: str, type_value: TypesValue) -> Union[int, str, list, None]:
            try:
                return self.config[section][option]
            except KeyError:
                raise NotFoundOption(section, option)

        def set(self, section: str, option: str, value: Union[int, str, list, None]) -> None:
            if section not in self.config:
                self.config[section] = {}

            self.config[section][option] = value

        def write_file(self, filename: str) -> None:
            self.filename_write = filename

    def test_simple_generate(self):
        reader = self.Reader()
        conf = Configuration(reader)

        conf.generate_simple()

        for section, options in Configuration._CONFIG_STRUCTURE.items():
            for option, option_prop in options.items():
                assert reader.get(section, option, option_prop['type']) == option_prop['simple']

    def test_get_attr(self):
        reader = self.Reader()
        conf = Configuration(reader)
        conf.generate_simple()

        for section, options in Configuration._CONFIG_STRUCTURE.items():
            for option, option_prop in options.items():
                assert getattr(conf, f'{section}_{option}') == reader.get(section, option, option_prop['simple'])

    def test_get_attr_error(self):
        reader = self.Reader()
        conf = Configuration(reader)

        with pytest.raises(AttributeError):
            tmp = conf.not_found_attr
