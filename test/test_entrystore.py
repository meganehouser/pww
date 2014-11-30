# coding: utf-8
from io import BytesIO
import json
import pytest
from pww.entrystore import EntryStore


store = None
data = None


class FakeCipher:
    def encrypt(self, plain):
        return plain

    def decrypt(self, encrypted):
        return encrypted


def setup():
    global store, data
    data = BytesIO()
    cipher = FakeCipher()
    store = EntryStore(data, cipher)


def teardown():
    data.close()


def test_initial_store_should_have_no_entries():
    assert len(store.entries) == 0


def test_load_store_should_have_entries():
    jsontxt = json.dumps({'title1': {'user': 'spam', 'pass': 'ham'}})
    with BytesIO(jsontxt.encode()) as b:
        store = EntryStore(b, FakeCipher())
        result = store.search('title1')

        assert len(result) == 1
        assert result['title1']['user'] == 'spam'


def test_adding_exists_entry_raise_exception():
    store.add('title', 'user', 'pass')
    with pytest.raises(Exception):
        store.add('title', 'dummy', 'dummy')


def test_entry_can_be_searched_by_title():
    store.add('title', 'user', 'pass')
    result = store.search('title')

    assert len(result) == 1
    assert result['title']['user'] == 'user'


def test_entry_can_be_searched_by_begins_with_match():
    store.add('title1', 'user1', 'pass1')
    store.add('title2', 'user2', 'pass2')
    store.add('dummy', 'userd', 'passd')
    result = store.search('title')

    assert len(result) == 2


def test_entry_can_be_chaned_values():
    store.add('title', 'user', 'pass')
    store.change('title', 'title', {'user': 'chusr'})

    entry = store.search('title')['title']
    assert entry['user'] == 'chusr'
    assert entry['password'] == 'pass'

def test_entry_can_be_changed_title():
    store.add('old_title', 'user', 'pass')
    store.change('old_title', 'new_title', {'user': 'chusr'})

    entries = store.search('old_title')
    assert len(entries) == 0

    entry = store.search('new_title')['new_title']
    assert entry['user'] == 'chusr'
    assert entry['password'] == 'pass'

def test_entries_can_be_saved():
    with BytesIO() as b:
        store = EntryStore(b, FakeCipher())
        store.add('title', 'usr', 'pass')
        store.save()

        buf = b.getbuffer()
        assert buf.nbytes > 0
