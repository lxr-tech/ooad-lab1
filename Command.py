from Factory import *

import sys
import argparse
from util import *


class AbstractCommand:
    def __init__(self, factory: AbstractFactory):
        self.factory = factory

    def execute(self):
        pass

    def cancel(self):
        pass


class OpenCommand(AbstractCommand):
    def __init__(self, factory: OpenFactory):
        super().__init__(factory)

    def execute(self):
        openTitle = self.factory.newContext()
        openTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ShowCommand(AbstractCommand):
    def __init__(self, factory: ShowFactory):
        super().__init__(factory=factory)

    def execute(self):
        showTitle = self.factory.newContext()
        showTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ListCommand(AbstractCommand):
    def __init__(self, factory: ListFactory):
        super().__init__(factory=factory)

    def execute(self):
        showTitle = self.factory.newContext()
        showTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ReadCommand(AbstractCommand):
    def __init__(self, factory: ReadFactory):
        super().__init__(factory=factory)

    def execute(self):
        readVisitor = self.factory.newContext()
        bookmark = sys.argv[2]
        readVisitor.strategyMethod(bookmark=bookmark)

    def cancel(self):
        super().cancel()


class AddTitleCommand(AbstractCommand):
    def __init__(self, factory: AddTitleFactory):
        super().__init__(factory=factory)

    def execute(self):
        addVisitor = self.factory.newContext()
        item, parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]
        addVisitor.strategyMethod(item=item, parent=parent)

    def cancel(self):
        pass  # need to be implemented in undo/redo


class AddBookmarkCommand(AbstractCommand):
    def __init__(self, factory: AddBookmarkFactory):
        super().__init__(factory=factory)

    def execute(self):
        addVisitor = self.factory.newContext()
        item, parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]
        addVisitor.strategyMethod(item=item, parent=parent)

    def cancel(self):
        pass  # need to be implemented in undo/redo


class DeleteCommand(AbstractCommand):
    def __init__(self, factory: DeleteFactory):
        super().__init__(factory=factory)

    def execute(self):
        deleteVisitor = self.factory.newContext()
        deleteVisitor.strategyMethod(name=sys.argv[2])

    def cancel(self):
        pass  # need to be implemented in undo/redo


class Invoker:
    def __init__(self):
        self.commandList = []

    def open(self):
        self.save()
        self.commandList = []
        openCommand = OpenCommand(OpenFactory())
        openCommand.execute()
        print('open interface')

    def showTree(self):
        showCommand = ShowCommand(ShowFactory())
        showCommand.execute()
        print('show interface')

    def listTree(self):
        showCommand = ListCommand(ListFactory())
        showCommand.execute()
        print('list interface')

    def read(self):
        readCommand = ReadCommand(ReadFactory())
        readCommand.execute()
        self.setCommand(readCommand)
        print('read interface')

    def addTitle(self):
        addCommand = AddTitleCommand(AddTitleFactory())
        addCommand.execute()
        self.setCommand(addCommand)
        print('add title interface')

    def addBookmark(self):
        addCommand = AddBookmarkCommand(AddBookmarkFactory())
        addCommand.execute()
        self.setCommand(addCommand)
        print('add title interface')

    def deleteTitle(self):
        deleteCommand = DeleteCommand(DeleteFactory)
        deleteCommand.execute()
        self.setCommand(deleteCommand)
        print('delete title interface')

    def deleteBookmark(self):
        deleteCommand = DeleteCommand(DeleteFactory)
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

