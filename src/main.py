#!/usr/bin/env python
import asyncio
from argparse import ArgumentParser, Namespace
from pathlib import Path

from config import Configuration, IniReader
from modules.add_timetable import add_timetable_from_site, add_timetable_from_html_file
from modules.generate_simple_config import generate_simple_config


def parse_argument(args: list[str] = None) -> Namespace:
    """Парсит аргументы командной строки.

    Args:
        args: Аргументы командной строки. Если не указано, то используется sys.argv.

    Returns:
        Спарсенные аргументы.
    """
    base_parser = ArgumentParser()
    base_parser.add_argument('--config', '-c', help='Path to config file', required=True, type=Path)
    base_parser.set_defaults(module='base')

    subparsers = base_parser.add_subparsers(description='modules')

    api_subparser = subparsers.add_parser('api')
    api_subparser.set_defaults(module='api')

    vkbot_subparser = subparsers.add_parser('vkbot')
    vkbot_subparser.set_defaults(module='vkbot')

    add_timetable_subparser = subparsers.add_parser('add-timetable')
    add_timetable_subparser.add_argument('--file', help='File with timetable. Support format: html, txt')
    add_timetable_subparser.set_defaults(module='add-timetable')

    simple_config_subparser = subparsers.add_parser('simple-config')
    simple_config_subparser.set_defaults(module='simple-config')

    return base_parser.parse_args(args)


def main() -> None:
    """Точка входа в приложение.
    """
    args = parse_argument()

    if args.module == 'simple-config':
        generate_simple_config(filename=args.config)
        return

    config = Configuration(IniReader.from_file(args.config))

    if args.module == 'add-timetable':
        if args.file:
            asyncio.run(add_timetable_from_html_file(config, args.file))
        else:
            asyncio.run(add_timetable_from_site(config))


if __name__ == '__main__':
    main()
