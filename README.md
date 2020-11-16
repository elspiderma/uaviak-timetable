# Бот для получения расписания УАвиаК

## Переменные окружения
 - `TOKEN_BOT` - VK API token
 - `DATA_BASE` - URL бызы данных (например `sqlite:///db.sqlite`, `postgresql://username:password@localhost/dbname`)
)
 - `ADMIN_ID` - ID пользователя-администратора
 - `LOG_LEVEL` - (optional) Уровень логов от 1 до 5.
   - 1 - logging.DEBUG,
   - 2 - logging.INFO,
   - 3 - logging.WARNING,
   - 4 - logging.ERROR,
   - 5 - logging.CRITICAL
 - `STATIC_DIR` - (optional) директория со статичными файлами
 - `TMPDIR` - (optional) директория с временными файлами
 
## Команды доступные только администратору
 - `upd` - рассылает расписание пользователям