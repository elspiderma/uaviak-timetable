class GetTimetableError(Exception):
    """Базовый класс для ошибок получения расписания с сайта УАвиаК'а."""
    pass


class GetHtmlError(GetTimetableError):
    """Ошибка сети при получении расписания."""
    def __init__(self, exception: Exception):
        """
        Args:
            exception: Ошибка.
        """
        self.exception = exception
        super().__init__(f'Error connection to site UAviaK. ({self.exception})')


class ParseTimetableError(GetTimetableError):
    """Ошибка парсинга расписнания."""
    def __init__(self, title: str, lessons: list[str]):
        """
        Args:
            title: Заголовок расписания.
            lessons: Массив уроков.
        """
        self.title = title
        self.lessons = lessons
        super().__init__(f'error parse timetable: {self.title}')


class ParseLessonError(GetTimetableError):
    """Ошибка парсинга пары."""
    def __init__(self, s: str):
        """
        Args:
            s: Строка урока.
        """
        self.line = s
        super().__init__(f'error parse line: {self.line}')
