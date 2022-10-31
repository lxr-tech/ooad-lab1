from Factory import *

import sys


class AbstractCommand:
    def __init__(self, execFactory: AbstractFactory, cnclFactory: AbstractFactory):
        self.execFactory = execFactory
        self.cnclFactory = cnclFactory

    def execute(self):
        pass

    def cancel(self):
        pass


class TreeCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)

    def execute(self):
        openTitle = self.execFactory.newContext()
        openTitle.strategyMethod()

    def cancel(self):
        super().cancel()


class ReadCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)

    def execute(self):
        readVisitor = self.execFactory.newContext()
        bookmark = sys.argv[2]
        readVisitor.strategyMethod(bookmark=bookmark)

    def cancel(self):
        super().cancel()


class AddCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)
        self.item, self.parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]

    def execute(self):
        addVisitor = self.execFactory.newContext()
        addVisitor.strategyMethod(item=self.item, parent=self.parent)

    def cancel(self):
        deleteVisitor = self.cnclFactory.newContext()
        deleteVisitor.strategyMethod(item=self.item)


class DeleteCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)
        self.item, self.parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]

    def execute(self):
        deleteVisitor = self.execFactory.newContext()
        deleteVisitor.strategyMethod(item=self.item)

    def cancel(self):
        addVisitor = self.cnclFactory.newContext()
        addVisitor.strategyMethod(item=self.item, parent=self.parent)


class Invoker:
    def __init__(self):
        self.undoList = []
        self.redoList = []

    def open(self):
        self.undoList = []
        self.redoList = []
        openCommand = TreeCommand(OpenFactory())
        openCommand.execute()

    def showTree(self):
        showCommand = TreeCommand(ShowFactory())
        showCommand.execute()

    def save(self):
        saveCommand = TreeCommand(SaveFactory())
        saveCommand.execute()

    def listTree(self):
        showCommand = TreeCommand(ListFactory())
        showCommand.execute()

    def read(self):
        readCommand = ReadCommand(ReadFactory())
        readCommand.execute()

    def addTitle(self):
        addCommand = AddCommand(AddTitleFactory(), DeleteTitleFactory())
        addCommand.execute()
        self.setUndoCommand(addCommand)

    def addBookmark(self):
        addCommand = AddCommand(AddBookmarkFactory(), DeleteBookmarkFactory())
        addCommand.execute()
        self.setUndoCommand(addCommand)

    def deleteTitle(self):
        deleteCommand = DeleteCommand(DeleteTitleFactory(), AddTitleFactory())
        deleteCommand.execute()
        self.setUndoCommand(deleteCommand)

    def deleteBookmark(self):
        deleteCommand = DeleteCommand(DeleteBookmarkFactory(), AddBookmarkFactory())
        deleteCommand.execute()
        self.setUndoCommand(deleteCommand)

    def undo(self):
        if self.undoList:
            command = self.undoList.pop()
            command.cancel()
            self.redoList.append(command)
        else:
            print("no command for undo")

    def redo(self):
        if self.redoList:
            command = self.redoList.pop()
            command.execute()
            self.undoList.append(command)
        else:
            print("no command for redo")

    def setUndoCommand(self, command: AbstractCommand):
        self.undoList.append(command)
        if self.redoList:
            self.redoList.clear()
