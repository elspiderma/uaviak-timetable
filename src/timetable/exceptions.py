class GetTimetableError(Exception):
    """Базовый класс для ошибок получения расписания с сайта УАвиаК'а."""
    pass


class GetHtmlError(GetTimetableError):
    """Ошибка сети при получении расписания."""
    def __init__(self, exceptions: Exception):
        self.exceptions = exceptions
        super().__init__(f'error connection to site UAviaK. ({self.exceptions})')


class ParseTimetableError(GetTimetableError):
    """Ошибка парсинга расписнания."""
    def __init__(self, title: str, info: str, lessons: list[str]):
        self.title = title
        self.info = info
        self.lessons = lessons
        super().__init__(f'error parse timetable: {self.title}')


class ParseLessonError(GetTimetableError):
    """Ошибка парсинга пары."""
    def __init__(self, s: str):
        self.line = s
        super().__init__(f'error parse line: {self.line}')


# Исключения связанные с запросами в БД.
class DataNotFoundError(Exception):
    """Подходящие данные не найдены."""
    pass
