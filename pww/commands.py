# coding: utf-8
import sys
from argparse import ArgumentParser
from .entrystore import EntryStore, PwwError
from .inputs import CLIInput


class Command:
    def __init__(self, title, homedir, _input):
        self.title = title
        self.home = homedir
        self._input = _input

    def execute(self, cmd):
        try:
            with EntryStore.load(self.home, self._input) as store:
                return cmd(self, store)
        except PwwError as err:
            print(err, file=sys.stderr)


class AddCommand(Command):
    def __call__(self):
        def cmd(_self, store):
            title, entry = self._input.get_entry_info({'title': self.title})
            store.add(title, **entry)
            store.save()

        super().execute(cmd)


class ShowCommand(Command):
    def __call__(self):
        def cmd(self, store):
            selector = self._input.entry_selector
            title, values = store.select_one(self.title, selector)
            print('title: ', title)
            print('user id: ', values['user'])
            print('password: ', values['password'])
            print('other: ', values['other'])
            return title, values

        return super().execute(cmd)

class ChangeCommand(Command):
    def __call__(self):
        def cmd(self, store):
            selector = self._input.entry_selector
            title, default = store.select_one(self.title, selector)
            default['title'] = title
            title, entry = self._input.get_entry_info(default)
            store.change(title, entry)
            store.save()

        super().execute(cmd)

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
