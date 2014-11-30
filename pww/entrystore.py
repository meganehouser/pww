# coding: utf-8
import json
from os import path
from contextlib import contextmanager
from .crypto import KeyProvider, Cipher

ENTRIES_FILE = 'entries'
USER_FILE = 'user'


class PwwError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class EntryStore:
    @staticmethod
    @contextmanager
    def load(home_dir, _input):
        """
        Load the EntryStore from the file in specific directory.
        home_dir: str
        """
        entries_path = path.join(home_dir, ENTRIES_FILE)
        user_path = path.join(home_dir, USER_FILE)

        def file_open(path):
            try:
                f = open(path, 'r+b')
            except FileNotFoundError:
                f = open(path, 'w+b')
            return f

        f = file_open(entries_path)
        u = file_open(user_path)
        try:
            key_provider = KeyProvider(u, _input)
            cipher = Cipher(*key_provider.get())
            yield EntryStore(f, cipher)
        finally:
            f.close()
            u.close()

    def __init__(self, data_file, cipher):
        """
        data_file:  BufferedIOBase
        """

        self.data_file = data_file
        self.cipher = cipher

        encrypted_data = self.data_file.read()
        if len(encrypted_data):
            plain_data = self.cipher.decrypt(encrypted_data)
            try:
                entries = json.loads(plain_data.decode())
            except UnicodeDecodeError:
                raise PwwError("pww can't read entries data. You may input invalid author info.")
        else:
            entries = {}

        self.entries = entries

    def add(self, title, user, password, other=None):
        """
        Method that add new entry to the store.
        """

        if title in self.entries.keys():
            raise PwwError('already stored')
        entry = {"user": user, "password": password, "other": other}
        self.entries[title] = entry

    def search(self, title_ptn):
        """
        Method that search entries by begins-with match.
        title_ptn: str
        """

        ptn = title_ptn.lower()

        def gen():
            for k in self.entries:
                if k.lower().startswith(ptn):
                    yield k, self.entries[k]

        return {k: v for k, v in gen()}

    def select_one(self, title_ptn, selector):
        entries = self.search(title_ptn)
        cnt = len(entries)
        if(cnt == 0):
            return None, None
        elif cnt == 1:
            t, v = list(entries.items())[0]
            return t, v.copy()
        else:
            t, v = selector(entries)
            return t, v.copy()

    def change(self, old_title, new_title, values):
        """
        Method that change entry values.
        title: str
        values: dict
        """
        if old_title == new_title:
            self.entries[old_title].update(values)
        else:
            entry = self.entries[old_title]
            entry.update(values)
            self.entries[new_title] = entry 
            del self.entries[old_title]

    def save(self):
        """
        Method that save entries.
        """

        json_data = json.dumps(self.entries)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        self.data_file.seek(0)
        self.data_file.truncate()
        self.data_file.write(encrypted_data)
