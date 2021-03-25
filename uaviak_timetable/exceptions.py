class GetHtmlError(Exception):
    def __init__(self, exceptions: Exception):
        self.exceptions = exceptions
        super().__init__(f'Error connection to site UAviaK. ({self.exceptions})')
