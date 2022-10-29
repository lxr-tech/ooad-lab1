from Factory import *

import sys




class AbstractCommand:
    def __init__(self, execFactory: AbstractFactory, cnclFactory: AbstractFactory):
        # execFactory用于执行命令
        # cnclFactory用于undo命令
        self.execFactory = execFactory
        self.cnclFactory = cnclFactory

    def execute(self):
        pass

    def cancel(self):
        pass

    # 没有用上
    def commit(self):
        pass


class TreeCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)

    def execute(self):
        openTitle = self.execFactory.newContext()
        openTitle.strategyMethod()

    def cancel(self):
        super().cancel()

    def commit(self):
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

    def commit(self):
        super().cancel()


class AddCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)
        # 如果没有指定父节点，则父节点为伪root节点
        self.item, self.parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]

    def execute(self):
        addVisitor = self.execFactory.newContext()
        addVisitor.strategyMethod(item=self.item, parent=self.parent)

    def cancel(self):
        deleteVisitor = self.cnclFactory.newContext()
        deleteVisitor.strategyMethod(item=self.item)

    def commit(self):
        pass  # need to be implemented in save


class DeleteCommand(AbstractCommand):
    def __init__(self, execFactory: AbstractFactory, cnclFactory=None):
        super().__init__(execFactory, cnclFactory)
        self.item, self.parent = sys.argv[2], None if len(sys.argv) < 4 else sys.argv[4]

    def execute(self):
        deleteVisitor = self.execFactory.newContext()
        deleteVisitor.strategyMethod(item=self.item)

    def cancel(self):
        # 如果delete掉了一个根目录，需要将原来的内容全部弄回去
        addVisitor = self.cnclFactory.newContext()
        addVisitor.strategyMethod(item=self.item, parent=self.parent)

    def commit(self):
        pass  # need to be implemented in save


class Invoker:
    def __init__(self):
        self.commandList = []    # undoList
        self.redoList = []

    def open(self):
        # self.save()
        self.commandList = []
        self.redoList = []
        openCommand = TreeCommand(OpenFactory())
        openCommand.execute()

    def showTree(self):
        showCommand = TreeCommand(ShowFactory())
        showCommand.execute()

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

    def save(self):
        # 获取数据库实例
        singleton = Singleton.getInstance()
        # 如果parentName=None，则是一级节点
        root_items = singleton.getChildren(parentName=None)
        # 获取一级节点的名字
        root_names = [root_item.getFullName() for root_item in root_items]
        # 通过dfs将书签树结构转为dict
        root_dict = [dfs_node(root_item, OrderedDict(), singleton) for root_item in root_items]
        # 哨兵节点
        fake_root = OrderedDict(zip(root_names, root_dict))
        # 通过dfs将dict转为markdown
        markdown_str = ''
        markdown_str = dfs_format(fake_root, 1, markdown_str)
        with open('save.bmk', 'w+') as f:
            f.write(markdown_str)


    def undo(self):
        # 如果commandList不为空
        if self.commandList:
            command = self.commandList.pop()
            command.cancel()
            # 将undo的命令添加至redoList
            self.redoList.append(command)
        else:
            print("no command for undo")

    def redo(self):
        if self.redoList:
            command = self.redoList.pop()
            command.execute()
            self.setUndoCommand(command)
        else:
            print("you should undo first to redo")


    def setUndoCommand(self, command: AbstractCommand):
        self.commandList.append(command)
        if self.redoList:
            self.redoList.clear()