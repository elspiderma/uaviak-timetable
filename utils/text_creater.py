class TextCreater:
    def __init__(self, *argv):
        self.lines = list(argv)

    def add(self, *argv):
        self.lines += argv

    def create(self):
        return '\n'.join(self.lines)

    def __str__(self):
        return self.create()

    def __repr__(self):
        return str(self.lines)
