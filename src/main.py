import asyncio
import datetime

from db import Database, ConnectionKeeper
from db.structures import Departaments
import parser


async def main():
    await ConnectionKeeper.init_connection('user', '1', 'uaviak', '127.0.0.1')

    conn = ConnectionKeeper.get_connection()
    db = Database(conn)

    with open('/media/hdd/data/uaviak site/21-06-21.html', 'r') as f:
        html_timetable = parser.HtmlTimetable(f.read())

    text_timetable = parser.TextTimetable.parse(html_timetable.parse_html()[1])

    await db.add_new_timetable_from_site(text_timetable.parse_text())

    await ConnectionKeeper.close_connection()


async def main2():
    await ConnectionKeeper.init_connection('user', '1', 'uaviak', '127.0.0.1')

    conn = ConnectionKeeper.get_connection()
    db = Database(conn)

    result = await db.get_timetable(datetime.date.fromisoformat('2021-06-22'), Departaments.FULL_TIME)
    print(result)

    await ConnectionKeeper.close_connection()


if __name__ == '__main__':
    asyncio.run(main2())