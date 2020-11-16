# Бот для получения расписания УАвиаК

## Переменные окружения
 - `TOKEN_BOT` - VK API token
 - `DATA_BASE` - URL бызы данных (например `sqlite:///db.sqlite`, `postgresql://username:password@localhost/dbname`)
)
 - `ADMIN_ID` - ID пользователя-администратора
 - `DEBUG_ENABLE` - (optional) Если 1, то включает режим отладки.
 - `STATIC_DIR` - (optional) директория со статичными файлами
 - `TMPDIR` - (optional) директория с временными файлами
 
## Команды доступные только администратору
 - `upd` - рассылает расписание пользователям