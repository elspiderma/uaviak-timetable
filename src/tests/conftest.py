from typing import Optional


class FakeInput:
    def __init__(self, answer: str):
        self.answer = answer
        self.prompt = None

    def input(self, prompt: Optional[str] = None) -> str:
        self.prompt = prompt
        return self.answer

    def __call__(self, *args, **kwargs) -> str:
        return self.input(*args, **kwargs)
