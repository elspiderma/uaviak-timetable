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

    def get(self):
        return '\n'.join(self.lines)
