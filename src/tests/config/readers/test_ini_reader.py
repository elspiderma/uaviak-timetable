import os
from configparser import ConfigParser

import pytest

from config import IniReader, TypesValue, NotFoundOption


class TestIniReader:
    def test_write_file_set(self, tmp_path):
        confparser = ConfigParser()
        filename = os.path.join(tmp_path, 'config.ini')

        reader = IniReader(ConfigParser())
        reader.set('test_string', 'test1', '')
        reader.set('test_string', 'test2', 'hello')
        reader.set('test_int', 'test1', 42)
        reader.set('test_list', 'test1', [])
        reader.set('test_list', 'test2', [42, 69])
        reader.set('test_list', 'test3', ['hello', 'world'])
        reader.set('test_none', 'test1', None)

        reader.write_file(filename)

        confparser.read(filename)
        assert confparser['test_string']['test1'] == ''
        assert confparser['test_string']['test2'] == 'hello'
        assert confparser['test_int']['test1'] == '42'
        assert confparser['test_list']['test1'] == ''
        assert confparser['test_list']['test2'] == '42,69'
        assert confparser['test_list']['test3'] == 'hello,world'
        assert confparser['test_none']['test1'] == ''

    def test_read_file_get(self, tmp_path):
        confparser = ConfigParser()
        filename = os.path.join(tmp_path, 'config.ini')

        confparser.read(filename)
        confparser.add_section('test_string')
        confparser.add_section('test_int')
        confparser.add_section('test_list')
        confparser.add_section('test_none')
        confparser.set('test_string', 'test1', '')
        confparser.set('test_string', 'test2', 'hello')
        confparser.set('test_int', 'test1', '42')
        confparser.set('test_list', 'test1', '')
        confparser.set('test_list', 'test2', '42,69')
        confparser.set('test_list', 'test3', 'hello,world')
        confparser.set('test_none', 'test1', '')
        with open(filename, 'w') as f:
            confparser.write(f)

        reader = IniReader.from_file(filename)
        assert reader.get('test_string', 'test1', TypesValue.STRING) is None
        assert reader.get('test_string', 'test2', TypesValue.STRING) == 'hello'
        assert reader.get('test_int', 'test1', TypesValue.INT) == 42
        assert reader.get('test_int', 'test1', TypesValue.STRING) == '42'
        assert reader.get('test_list', 'test1', TypesValue.LIST) is None
        assert reader.get('test_list', 'test2', TypesValue.LIST) == ['42', '69']
        assert reader.get('test_list', 'test2', TypesValue.STRING) == '42,69'
        assert reader.get('test_list', 'test3', TypesValue.LIST) == ['hello', 'world']
        assert reader.get('test_none', 'test1', TypesValue.STRING) is None

    def test_error_type_set(self):
        reader = IniReader(ConfigParser())

        with pytest.raises(TypeError):
            reader.set('test', 'test', ('error',))

        with pytest.raises(TypeError):
            reader.set('test', 'test', {1, 2})

    def test_not_found_section(self):
        reader = IniReader(ConfigParser())

        with pytest.raises(NotFoundOption) as e:
            reader.get('notfound', 'notfound2', TypesValue.STRING)

        assert e.value.section == 'notfound'
        assert e.value.option == 'notfound2'

    def test_not_found_option(self):
        reader = IniReader(ConfigParser())
        reader.set('found', 'found', '')

        with pytest.raises(NotFoundOption) as e:
            reader.get('found', 'notfound', TypesValue.STRING)

        assert e.value.section == 'found'
        assert e.value.option == 'notfound'
