import os
from pathlib import Path
import environ
from hashids import Hashids


class HashidHandler:
    def __init__(self):
        env = environ.Env()
        BASE_DIR = Path(__file__).resolve().parent.parent
        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
        salt = env("SALT")

        self.hashids = Hashids(salt=salt, min_length=6)

    def encode_hash(self, id):
        return self.hashids.encode(id)

    def decode_hash(self, hash):
        return self.hashids.decode(hash)
