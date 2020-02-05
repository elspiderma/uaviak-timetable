from vk_bot.keyboard.buttons.button_text import ButtonText
import json


class Keyboard:
    def __init__(self, one_time: bool = True, inline: bool = False, size_row: int = 5):
        self.one_time = one_time
        self.inline = inline
        self.size_row = size_row

        self.buttons = []

    def __is_full_last_row(self):
        if len(self.buttons) == 0:
            return True
        elif len(self.buttons[-1]) == self.size_row:
            return True
        else:
            return False

    def add(self, *argv, continue_row: bool = True):
        if not self.__is_full_last_row() and continue_row:
            row = self.buttons.pop()
        else:
            row = []

        i = len(row) + 1
        for button in argv:
            row.append(button)

            if i == self.size_row:
                self.row(*row)
                row = []
                i = 0

            i += 1

        if len(row) > 0:
            self.row(*row)

    def row(self, *args):
        row = []

        for button in args:
            if isinstance(button, str):
                row.append(ButtonText(label=button))
            else:
                row.append(button)

        self.buttons.append(row)

    def to_dict(self):
        dict_json = dict()

        if self.inline is False:
            dict_json['one_time'] = self.one_time

        dict_json['inline'] = self.inline
        dict_json['buttons'] = []

        for row in self.buttons:
            row_dict = []

            for button in row:
                row_dict.append(button.to_dict())

            dict_json['buttons'].append(row_dict)

        return dict_json

    def to_json(self):
        return json.dumps(self.to_dict())
