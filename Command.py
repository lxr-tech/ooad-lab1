from Factory import *

import sys
import argparse
from util import *


class AbstractCommand:
    def __init__(self):
        pass

    def execute(self):
        pass


class OpenCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.openFactory = OpenFactory()

    def execute(self):
        openTitle = self.openFactory.newTitleVisitor()
        component = markdown_to_dict(sys.argv[2])
        singleton = Singleton.getInstance()
        openTitle.visit(singleton.getRoot(), raw_dict=component)


class ShowCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.showFactory = ShowFactory()

    def execute(self):
        showTitle = self.showFactory.newTitleVisitor()
        singleton = Singleton.getInstance()
        showTitle.visit(singleton.getRoot())


class ListCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.listFactoty = ListFactory()

    def execute(self):
        showTitle = self.listFactoty.newTitleVisitor()
        singleton = Singleton.getInstance()
        showTitle.visit(singleton.getRoot())


class ReadCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.readFactory = ReadFactory()

    def execute(self):
        readVisitor = self.readFactory.newBookmarkVisitor()
        singleton = Singleton.getInstance()
        bookmark = sys.argv[2]
        readVisitor.visit(singleton.getRoot(), bookmark=bookmark)


class AddCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.addFactory = AddFactory()

    def execute(self):
        addVisitor = self.addFactory.newTitleVisitor()
        singleton = Singleton.getInstance()
        if sys.argv[1] == 'add-title':
            addVisitor.visit(singleton.getRoot(), title=sys.argv[2],
                             parent=None if len(sys.argv) < 4 else sys.argv[4])
        elif sys.argv[1] == 'add-bookmark':
            singleton = Singleton.getInstance()
            addVisitor.visit(singleton.getRoot(), bookmark=sys.argv[2],
                             parent=None if len(sys.argv) < 4 else sys.argv[4])


class DeleteCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.deleteFactory = DeleteFactory()

    def execute(self):
        deleteVisitor = self.deleteFactory.newTitleVisitor()
        singleton = Singleton.getInstance()
        deleteVisitor.visit(singleton.getRoot(), name=sys.argv[2])


class Invoker:
    def __init__(self):
        self.commandList = []

    def open(self):
        self.save()
        self.commandList = []
        openCommand = OpenCommand()
        openCommand.execute()
        print('open interface')

    def showTree(self):
        showCommand = ShowCommand()
        showCommand.execute()
        print('show interface')

    def listTree(self):
        showCommand = ListCommand()
        showCommand.execute()
        print('list interface')

    def read(self):
        readCommand = ReadCommand()
        readCommand.execute()
        self.setCommand(readCommand)
        print('read interface')

    def add(self):
        addCommand = AddCommand()
        addCommand.execute()
        self.setCommand(addCommand)
        print('add title interface')

    def delete(self):
        deleteCommand = DeleteCommand()
        deleteCommand.execute()
        self.setCommand(deleteCommand)
        print('delete title interface')

    def save(self):
        # for command in self.commandList:
        #     command.execute()
        print('save interface')
        pass

    def undo(self):
        print('undo interface')
        pass

    def redo(self):
        print('redo interface')
        pass

    def setCommand(self, command: AbstractCommand):
        self.commandList.append(command)

