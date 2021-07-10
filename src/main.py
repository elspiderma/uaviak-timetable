#!/usr/bin/env python
import datetime
from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

import uaviak_parser
from config import generate_simple_config
from db import Database, ConnectionKeeper
from db.structures import Departaments

if TYPE_CHECKING:
    from config import Configuration


def parse_argument(args: list[str] = None):
    """Парсит аргументы командной строки.

    Args:
        args: Аргументы командной строки. Если не указано, то используется sys.argv.

    Returns:
        Спарсенные аргументы.
    """
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='path to config file', required=True, type=Path)
    parser.add_argument('--module', choices=['api', 'vkbot', 'updater', 'simple-config'], required=True)

    return parser.parse_args(args)


def main():
    args = parse_argument()

    if args.module == 'simple-config':
        generate_simple_config(filename=args.config)


async def main3(conf: 'Configuration'):
    await ConnectionKeeper.init_connection(
        conf.postgres_login, conf.postgres_password, conf.postgres_database, conf.postgres_ip
    )

    conn = ConnectionKeeper.get_connection()
    db = Database(conn)

    with open('/media/hdd/data/uaviak site/21-06-21.html', 'r') as f:
        html_timetable = uaviak_parser.HtmlTimetable(f.read())

    text_timetable = uaviak_parser.TextTimetable.parse(html_timetable.parse_html()[1])

    await db.add_new_timetable(text_timetable.parse_html())

    await ConnectionKeeper.close_connection()


if __name__ == '__main__':
    main()
