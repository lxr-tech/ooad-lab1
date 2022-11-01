import re

from Component import *
from Viewer import *


class CreateStrategy:

    def create(self, item, parent):
        pass


class Creator:

    def __init__(self, createStrategy: CreateStrategy):
        self.createStrategy = createStrategy

    def setStrategy(self, createStrategy: CreateStrategy):
        self.createStrategy = createStrategy

    def create(self, item, parent):
        self.createStrategy.create(item, parent)


class AddBookmarkStrategy(CreateStrategy):

    def create(self, item: str, parent: str):
        itemList = item.split('@')
        assert len(itemList) == 2
        bookmark = BookmarkTitle(name=itemList[0], url=itemList[1], root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(bookmark)


class CreateBookmarkStrategy(CreateStrategy):

    def create(self, item: str, parent: str):
        name = re.findall(r'\[.+?\]', item)[0].replace('[', '').replace(']', '')
        url = re.findall(r'\(.+?\)', item)[0].replace('(', '').replace(')', '')
        bookmark = BookmarkTitle(name=name, url=url, root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(bookmark)


class CreateBookmarkListStrategy(CreateStrategy):

    def __init__(self):
        super().__init__()
        self.createStrategy = CreateBookmarkStrategy()

    def create(self, item: str, parent: str):
        if item in [' ', '']:
            return
        itemList = item.split('\n')
        for singleItem in itemList:
            self.createStrategy.create(item=singleItem, parent=parent)


class CreateTitleStrategy(CreateStrategy):

    def create(self, item: str, parent: str):
        title = BookmarkTitle(name=item, root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(title)


class DeleteStrategy:

    def delete(self, item):
        pass


class Deleter:

    def __init__(self, deleteStrategy: DeleteStrategy):
        self.deleteStrategy = deleteStrategy

    def setStrategy(self, deleteStrategy: DeleteStrategy):
        self.deleteStrategy = deleteStrategy

    def delete(self, item):
        self.deleteStrategy.delete(item)


class DeleteBookmarkStrategy(DeleteStrategy):

    def delete(self, item: str):
        singleton = Singleton.getInstance()
        singleton.deleteComponent(name=item)


class DeleteTitleStrategy(DeleteStrategy):

    def delete(self, item: str):
        singleton = Singleton.getInstance()
        children = singleton.getChildren(parentName=item)
        contentProvider = ContentProvider()
        for child in children:
            deleter = Deleter(DeleteBookmarkStrategy() if contentProvider.isDirectory(child) else DeleteTitleStrategy())
            deleter.delete(item=child.getName())
        singleton.deleteComponent(name=item)


