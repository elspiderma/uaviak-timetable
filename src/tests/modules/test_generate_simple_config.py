import os

from modules.generate_simple_config import generate_simple_config


class TestGenerateSimpleConfig:
    def test_generate_simple_config(self, tmp_path):
        filename = os.path.join(tmp_path, 'config.ini')

        generate_simple_config(filename)

        assert os.path.isfile(filename)
        with open(filename, 'r') as f:
            assert f != ''

    def test_generate_simple_config_overwrite_yes(self, monkeypatch, tmp_path):
        monkeypatch.setattr('modules.generate_simple_config.ask_yes_no', lambda *args: True)

        filename = os.path.join(tmp_path, 'config.ini')
        with open(filename, 'w') as f:
            f.write('old data')

        generate_simple_config(filename)

        with open(filename, 'r') as f:
            assert f.read() != 'old data'

    def test_generate_simple_config_overwrite_no(self, monkeypatch, tmp_path):
        monkeypatch.setattr('modules.generate_simple_config.ask_yes_no', lambda *args: False)

        filename = os.path.join(tmp_path, 'config.ini')
        with open(filename, 'w') as f:
            f.write('old data')

        generate_simple_config(filename)

        with open(filename, 'r') as f:
            assert f.read() == 'old data'
