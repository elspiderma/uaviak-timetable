#!/usr/bin/env python
import asyncio
from argparse import ArgumentParser
from pathlib import Path

from config import Configuration, IniReader
from modules.add_timetable import add_timetable_from_site
from modules.generate_simple_config import generate_simple_config


def parse_argument(args: list[str] = None):
    """Парсит аргументы командной строки.

    Args:
        args: Аргументы командной строки. Если не указано, то используется sys.argv.

    Returns:
        Спарсенные аргументы.
    """
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='path to config file', required=True, type=Path)
    parser.add_argument('--module', choices=['api', 'vkbot', 'add-timetable', 'simple-config'], required=True)

    return parser.parse_args(args)


def main():
    args = parse_argument()

    if args.module == 'simple-config':
        generate_simple_config(filename=args.config)
        return

    config = Configuration(IniReader.from_file(args.config))

    if args.module == 'add-timetable':
        asyncio.run(add_timetable_from_site(config))


if __name__ == '__main__':
    main()
