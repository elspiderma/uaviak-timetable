from typing import List


class MultilineText:
    def __init__(self):
        self.lines = []

    def add_line(self, *lines, insert_in_begin=False):
        if insert_in_begin:
            lines = lines[::-1]

        for i in lines:
            if insert_in_begin:
                self.lines.insert(0, i)
            else:
                self.lines.append(i)

    def get(self, sep='\n') -> str:
        return sep.join(self.lines)

    def __str__(self):
        return self.get()


class GroupMultilineText:
    def __init__(self):
        self.multiline_text: List[MultilineText] = []

    def get(self, sep='\n\n') -> str:
        lines = [i.get() for i in self.multiline_text]
        return sep.join(lines)

    def add_line(self, *lines, insert_in_begin=False):
        if len(self.multiline_text) == 0:
            self.new_group()

        self.multiline_text[-1].add_line(*lines, insert_in_begin=insert_in_begin)

    def new_group(self):
        self.multiline_text.append(MultilineText())
