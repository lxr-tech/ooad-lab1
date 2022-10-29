import sys
import util
from Command import *

func_dict = {'add-title': 'invoker.addTitle',               # ok (almost, chinese character)
             'add-bookmark': 'invoker.addBookmark',         # ok
             'delete-title': 'invoker.deleteTitle',         # ok
             'delete-bookmark': 'invoker.deleteBookmark',   # ok
             'open': 'invoker.open',                        # ok
             'save': 'invoker.save',                        #
             'undo': 'invoker.undo',                        #
             'redo': 'invoker.redo',                        #
             'show-tree': 'invoker.showTree',               # ok
             'ls-tree': 'invoker.listTree',                 # ok (nearly, folder problem)
             'read-bookmark': 'invoker.read', }             # ok


class Controller:

    @staticmethod
    def main():
        invoker = Invoker()
        args_ = get_input()
        while len(args_) > 0 and not args_[0].__contains__('exit'):
            sys.argv.extend(args_)
            try:
                eval(func_dict[sys.argv[1]])()
            except (NameError, KeyError):
                print('this is an undefined command')
            args_ = get_input()


if __name__ == '__main__':
    Controller.main()
    '''
        open test.bmk
        add-title A
        show-tree
        save
    '''
