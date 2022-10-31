import util
from Command import *

func_dict = {'add-title': 'invoker.addTitle',               # ok (almost, chinese character)
             'add-bookmark': 'invoker.addBookmark',         # ok
             'delete-title': 'invoker.deleteTitle',         # ok
             'delete-bookmark': 'invoker.deleteBookmark',   # ok
             'open': 'invoker.open',                        # ok
             'save': 'invoker.save',                        # ok
             'undo': 'invoker.undo',                        # ok
             'redo': 'invoker.redo',                        # ok
             'show-tree': 'invoker.showTree',               # ok
             'ls-tree': 'invoker.listTree',                 # ok (nearly, folder problem)
             'read-bookmark': 'invoker.read', }             # ok


class Controller:

    @staticmethod
    def main():
        invoker = Invoker()
        argv = get_input()
        while len(argv) > 0 and not argv[0].__contains__('exit'):
            update_sys_argv(argv)
            try:
                eval(func_dict[argv[0]])()
            except (NameError, KeyError):
                print('this is an undefined command')
            argv = get_input()


if __name__ == '__main__':
    Controller.main()
