import sys
import argparse


def add_title():
    parser = argparse.ArgumentParser()
    parser.add_argument("-add_title", help="add sth.")
    parser.add_argument("-at", help="at sp.")
    args = parser.parse_args()
    print(f"this is an add_title function, info: {{add: {args.add_title}, at: {args.at}, }}")


def add_bookmark():
    parser = argparse.ArgumentParser()
    parser.add_argument("-add_bookmark", help="add sth.")
    parser.add_argument("-at", help="at sp.")
    args = parser.parse_args()
    print(f"this is an add_bookmark function, info: {{add: {args.add_bookmark}, at: {args.at}, }}")


def delete():
    parser = argparse.ArgumentParser()
    parser.add_argument("-delete", help="delete sth.")
    args = parser.parse_args()
    print(f"this is a delete function, info: {{delete: {args.delete}, }}")


def open_():
    parser = argparse.ArgumentParser()
    parser.add_argument("-open", help="open sth.")
    args = parser.parse_args()
    print(f"this is an open function, info: {{open: {args.open}, }}")


def save():
    print(f'this is a save function, info: {{}}')


def undo():
    print(f'this is an undo function, info: {{}}')


def redo():
    print(f'this is a redo function, info: {{}}')


def show_tree():
    print(f'this is a show_tree function, info: {{}}')


def ls_tree():
    print(f'this is a ls_tree function, info: {{}}')


def read_bookmark():
    parser = argparse.ArgumentParser()
    parser.add_argument("-read_bookmark", help="read sth.")
    args = parser.parse_args()
    print(f'this is a read_bookmark function, info: {{read: {args.read_bookmark}, }}')


def undefined():
    print('this is an undefined function')


# todo: add (add-title [at], add-bookmark [at], )
#       delete (delete-title, delete-bookmark, )
#       open, bookmark, edit
#       save, undo, redo
#       show-tree, ls-tree,
#       read-bookmark

func_dict = {'-add_title': add_title, '-add_bookmark': add_bookmark, '-delete': delete,
             '-open': open_, '-save': save, '-undo': undo, '-redo': redo,
             '-show_tree': show_tree, '-ls_tree': ls_tree, '-read_bookmark': read_bookmark, }


def get_input():
    sys.argv = [sys.argv[0]]
    args = input(">>> ").split()
    args = [item if i % 2 == 1 else '-' + item.replace('-', '_') for (i, item) in enumerate(args)]
    return args


if __name__ == '__main__':
    args_ = get_input()
    while not args_[0].__contains__('exit'):
        sys.argv.extend(args_)
        try:
            func_dict[args_[0]]()
        except KeyError:
            undefined()
        args_ = get_input()
