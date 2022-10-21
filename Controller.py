import sys
from Command import *

func_dict = {'add-title': 'invoker.add',            # ok (almost, chinese character)
             'add-bookmark': 'invoker.add',         # ok
             'delete-title': 'invoker.delete',      # ok
             'delete-bookmark': 'invoker.delete',   # ok
             'open': 'invoker.open',                # ok
             'save': 'invoker.save',                #
             'undo': 'invoker.undo',                #
             'redo': 'invoker.redo',                #
             'show-tree': 'invoker.showTree',       # ok
             'ls-tree': 'invoker.listTree',         # ok (nearly, folder)
             'read-bookmark': 'invoker.read', }     # ok


class Controller:

    @staticmethod
    def get_input():
        sys.argv = [sys.argv[0]]
        args = input(">>> ").replace('\'', '').replace('\"', '').split()
        return args

    @staticmethod
    def main():
        invoker = Invoker()
        args_ = Controller.get_input()
        while not args_[0].__contains__('exit'):
            sys.argv.extend(args_)
            try:
                eval(func_dict[sys.argv[1]])()
            except (NameError, KeyError):
                print('this is an undefined command')
            args_ = Controller.get_input()


if __name__ == '__main__':
    Controller.main()
