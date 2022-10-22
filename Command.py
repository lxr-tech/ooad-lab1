from Factory import *

import sys
import argparse
from util import *


class AbstractCommand:
    def __init__(self):
        pass

    def execute(self):
        pass

    def cancel(self):
        pass


class OpenCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.openFactory = OpenFactory()

    def execute(self):
        openTitle = self.openFactory.newContext()
        component = markdown_to_dict(sys.argv[2])
        openTitle.strategyMethod(raw_dict=component)

    def cancel(self):
        super().cancel()


class ShowCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.showFactory = ShowFactory()

    def execute(self):
        showTitle = self.showFactory.newContext()
        showTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ListCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.listFactory = ListFactory()

    def execute(self):
        showTitle = self.listFactory.newContext()
        showTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ReadCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.readFactory = ReadFactory()

    def execute(self):
        readVisitor = self.readFactory.newContext()
        bookmark = sys.argv[2]
        readVisitor.strategyMethod(bookmark=bookmark)

    def cancel(self):
        super().cancel()


class AddCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.addFactory = AddFactory()

    def execute(self):
        pass
        # addVisitor = self.addFactory.newContext()
        # if sys.argv[1] == 'add-title':
        #     addVisitor.strategyMethod(title=sys.argv[2],
        #                               parent=None if len(sys.argv) < 4 else sys.argv[4])
        # elif sys.argv[1] == 'add-bookmark':
        #     addVisitor.strategyMethod(bookmark=sys.argv[2],
        #                               parent=None if len(sys.argv) < 4 else sys.argv[4])

    def cancel(self):
        pass  # need to be implemented in undo/redo


class DeleteCommand(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.deleteFactory = DeleteFactory()

    def execute(self):
        deleteVisitor = self.deleteFactory.newContext()
        deleteVisitor.strategyMethod(name=sys.argv[2])

    def cancel(self):
        pass  # need to be implemented in undo/redo


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

