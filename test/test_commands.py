# coding: utf-8

from pww.commands import (CommandFactory,
                          AddCommand,
                          ShowCommand,
                          ChangeCommand)


class FakeInput:
    def __init__(self, **kwargs):
        self.dic = kwargs

    def get_user_name(self):
        return self.dic.get('salt_id', '')

    def get_password(self):
        return self.dic.get('cipher_pass', '')

    def entry_selector(self, entries):
        title = list(entries.keys())[0]
        return title, entries[title]

    def get_entry_info(self, default={}):
        title = self.dic.get('title', '')
        entry = {'user': self.dic.get('user', ''),
                 'password': self.dic.get('password', ''),
                 'other': self.dic.get('other', '')}
        return title, entry


class TestCreateCommand:
    def setup_method(self, method):
        self.factory = CommandFactory('')

    def test_add_arg_should_create_AddCommand(self):
        argv = ['add', 'title1']
        command = self.factory.create(argv)
        assert type(command) == AddCommand

    def test_show_arg_should_create_ShowCommand(self):
        argv = ['show', 'title1']
        command = self.factory.create(argv)
        assert type(command) == ShowCommand

    def test_change_arg_should_create_ChangeCommand(self):
        argv = ['change', 'title1']
        command = self.factory.create(argv)
        assert type(command) == ChangeCommand


class TestExecuteCommand:
    def test_show_added_entry(self, tmpdir):
        factory = CommandFactory(tmpdir.strpath)

        ini_entry = dict(salt_id='spam',
                         cipher_pass='salt',
                         user='hoge',
                         password='ham',
                         title='abcde')

        show_constraint = dict(cipher_pass='salt', title='abcde')

        add = factory.create(['add'], FakeInput(**ini_entry))
        show = factory.create(['show'], FakeInput(**show_constraint))

        add()
        title, entry = show()
        assert title == 'abcde'
        assert entry == {'user': 'hoge', 'password': 'ham', 'other': ''}

    def test_change_added_entry(self, tmpdir):
        factory = CommandFactory(tmpdir.strpath)

        ini_entry = dict(salt_id='spam',
                         cipher_pass='salt',
                         user='hoge',
                         password='ham',
                         title='abcde')
        change_info = dict(cipher_pass='salt',
                           title='abcde',
                           user='fuga',
                           password='changed',
                           other='aaaaa')
        show_constraint = dict(cipher_pass='salt',
                               title='abcde')

        add = factory.create(['add'], FakeInput(**ini_entry))
        change = factory.create(['change'], FakeInput(**change_info))
        show = factory.create(['show'], FakeInput(**show_constraint))

        add()
        change()
        title, entry = show()
        assert entry == {'user': 'fuga', 'password': 'changed', 'other': 'aaaaa'}
