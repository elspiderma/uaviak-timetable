import os
from hashlib import sha256

import config


class HashFile:
    HASH_DIR = os.path.join(config.TMPDIR, 'hash')

    def __init__(self, hashname: str):
        self.hashname = hashname
        self.filename_with_hash = os.path.join(self.__class__.HASH_DIR, self.hashname)

        self.__class__.create_hash_dir()

    @classmethod
    def create_hash_dir(cls):
        if not os.path.exists(cls.HASH_DIR):
            if os.path.isfile(cls.HASH_DIR):
                raise FileExistsError(f'{cls.HASH_DIR} not a directory')

            os.mkdir(cls.HASH_DIR)

    def is_change(self, text: str) -> bool:
        if not os.path.exists(self.filename_with_hash):
            return True

        newhash = sha256(text.encode('utf-8')).hexdigest()
        with open(self.filename_with_hash, 'r') as f:
            oldhash = f.read()

        return oldhash != newhash

    def edit(self, text: str):
        newhash = sha256(text.encode('utf-8')).hexdigest()
        with open(self.filename_with_hash, 'w') as f:
            f.write(newhash)

    def __repr__(self):
        return f'<hash {self.hashname}>'
