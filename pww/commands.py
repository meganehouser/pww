# coding: utf-8
from argparse import ArgumentParser
from .entrystore import EntryStore
from .inputs import CLIInput


class AddCommand:
    def __init__(self, title, homedir, _input):
        self.title = title
        self.home = homedir
        self._input = _input

    def __call__(self):
        with EntryStore.load(self.home, self._input) as store:
            title, entry = self._input.get_entry_info({'title': self.title})
            store.add(title, **entry)
            store.save()


class ShowCommand:
    def __init__(self, title, homedir, _input):
        self.title = title
        self.home = homedir
        self._input = _input

    def __call__(self):
        with EntryStore.load(self.home, self._input) as store:
            selector = self._input.entry_selector
            title, values = store.select_one(self.title, selector)
            print('title: ', title)
            print('user id: ', values['user'])
            print('password: ', values['password'])
            print('other: ', values['other'])
            return title, values


class ChangeCommand:
    def __init__(self, title, homedir, _input):
        self.title = title
        self.home = homedir
        self._input = _input

    def __call__(self):
        with EntryStore.load(self.home, self._input) as store:
            selector = self._input.entry_selector
            title, default = store.select_one(self.title, selector)
            default['title'] = title
            title, entry = self._input.get_entry_info(default)
            store.change(title, entry)
            store.save()


class CommandFactory:
    def __init__(self, home):
        self.home = home
        self.parser = ArgumentParser(description='password manager')
        sub = self.parser.add_subparsers(dest='command_name')

        add = sub.add_parser('add')
        add.add_argument('title', nargs='?', default='')
        add.set_defaults(func=AddCommand)

        show = sub.add_parser('show')
        show.add_argument('title', nargs='?', default='')
        show.set_defaults(func=ShowCommand)

        change = sub.add_parser('change')
        change.add_argument('title', nargs='?', default='')
        change.set_defaults(func=ChangeCommand)

    def create(self, argv, _input=CLIInput()):
        args = self.parser.parse_args(argv)

        if not args.command_name:
            raise Exception('invalid argv')

        return args.func(args.title, self.home, _input)
