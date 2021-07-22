from tests.conftest import FakeInput

from utils import ask_yes_no


class TestAskYesNo:
    YES_ANSWERS = ('y', 'yes', '1', 'YES', 'Y', 'yEs')
    NO_ANSWERS = ('n', 'no', '0', 'NO', 'N', 'nO')

    def test_ask_yes_no_answer_yes(self, monkeypatch):
        text_q = 'test text'

        for i in self.YES_ANSWERS:
            fake_input = FakeInput(i)

            with monkeypatch.context() as m:
                m.setattr('builtins.input', fake_input)

                result = ask_yes_no(text_q)

            assert result is True

    def test_ask_yes_no_answer_no(self, monkeypatch):
        text_q = 'test text'

        for i in self.NO_ANSWERS:
            fake_input = FakeInput(i)

            with monkeypatch.context() as m:
                m.setattr('builtins.input', fake_input)

                result = ask_yes_no(text_q)

            assert result is False

    def test_ask_yes_prompt(self, monkeypatch):
        text_q = 'test text'
        fake_input_false = FakeInput('y')
        fake_input_true = FakeInput('y')

        with monkeypatch.context() as m:
            m.setattr('builtins.input', fake_input_false)
            ask_yes_no(text_q, False)

        with monkeypatch.context() as m:
            m.setattr('builtins.input', fake_input_true)
            ask_yes_no(text_q, True)

        assert fake_input_false.prompt == f'{text_q} (y/N): '
        assert fake_input_true.prompt == f'{text_q} (Y/n): '
