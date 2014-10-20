# coding: utf-8

from getpass import getpass


class CLIInput():
    def get_user_name(self):
        return input('user name: ')

    def get_password(self):
        return getpass()

    def entry_selector(self, entries):
        if not entries:
            return None, None

        titles = list(entries.keys())

        for i, title in enumerate(titles):
            print('[{0}] {1}'.format(i, title))

        number = input('> ')
        if number.isdigit() and int(number) <= len(titles):
            title = titles[int(number)]
            return title, entries[title]
        else:
            return None, None

    def get_entry_info(self, default={}):
        entry = {}

        def getter(name):
            default_value = default.get(name)
            default_value = '' if default_value else default_value
            return input('{0} [{1}]: '.format(name, default_value))

        title = getter('title')
        keys = ['user', 'password', 'other']
        for key in keys:
            entry[key] = getter(key)

        return title, entry
