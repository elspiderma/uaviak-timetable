import os
from argparse import Namespace

from modules import GenerateConfigModule


class TestGenerateSimpleConfig:
    def test_generate_simple_config(self, tmp_path):
        filename = os.path.join(tmp_path, 'config.ini')
        gcm = GenerateConfigModule(Namespace(module='simple-config', config=filename))

        gcm.run()

        assert os.path.isfile(filename)
        with open(filename, 'r') as f:
            assert f != ''

    def test_generate_simple_config_overwrite_yes(self, monkeypatch, tmp_path):
        monkeypatch.setattr('modules.generate_config_module.ask_yes_no', lambda *args: True)
        filename = os.path.join(tmp_path, 'config.ini')
        gcm = GenerateConfigModule(Namespace(module='simple-config', config=filename))

        with open(filename, 'w') as f:
            f.write('old data')

        gcm.run()

        with open(filename, 'r') as f:
            assert f.read() != 'old data'

    def test_generate_simple_config_overwrite_no(self, monkeypatch, tmp_path):
        monkeypatch.setattr('modules.generate_config_module.ask_yes_no', lambda *args: False)
        filename = os.path.join(tmp_path, 'config.ini')
        gcm = GenerateConfigModule(Namespace(module='simple-config', config=filename))

        with open(filename, 'w') as f:
            f.write('old data')

        gcm.run()

        with open(filename, 'r') as f:
            assert f.read() == 'old data'
