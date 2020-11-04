# Бот для получения расписания УАвиаК

## Переменные окружения
 - `TOKEN_BOT` - VK API token
 - `DATA_BASE` - URL бызы данных (например `sqlite:///db.sqlite`, `postgresql://username:password@localhost/dbname`)
)
 - `STATIC_DIR` - (optional) директория со статичными файлами
 - `ADMIN_ID` - ID пользователя-администратора
 
## Команды доступные только администратору
 - `upd` - рассылает расписание пользователям