import os
from hashlib import sha256

import config


class HashFile:
    """Класс для сравнения текстовых данный по хешу."""
    HASH_DIR = os.path.join(config.TMPDIR, 'hash') # Директория с хешами

    def __init__(self, hashname: str):
        """
        @param hashname: Имя хеша
        """
        self.hashname = hashname
        self.filename_with_hash = os.path.join(self.__class__.HASH_DIR, self.hashname)

        self.__class__.create_hash_dir()

    @classmethod
    def create_hash_dir(cls):
        """Создает папку с для хранения хешей.

        @raise FileExistsError: Невозможно создать директорию, из-за того, что уже существует файл с таким названием.
        """
        if not os.path.exists(cls.HASH_DIR):
            if os.path.isfile(cls.HASH_DIR):
                raise FileExistsError(f'{cls.HASH_DIR} not a directory')

            os.mkdir(cls.HASH_DIR)

    def is_change(self, text: str) -> bool:
        """Проверяет, изменился ли текст.

        @param text: Текст для проверки.
        @return: True - если изменился, иначе False
        """
        if not os.path.exists(self.filename_with_hash):
            return True

        newhash = sha256(text.encode('utf-8')).hexdigest()
        with open(self.filename_with_hash, 'r') as f:
            oldhash = f.read()

        return oldhash != newhash

    def edit(self, text: str):
        """Сохраняет новый хеш

        @param text: Текст, по которому будет создан хеш.
        """
        newhash = sha256(text.encode('utf-8')).hexdigest()
        with open(self.filename_with_hash, 'w') as f:
            f.write(newhash)

    def __repr__(self):
        return f'<hash {self.hashname}>'
