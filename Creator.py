import re

from Component import *


class CreateStrategy:

    def create(self, item, parent) -> BookmarkTitle:
        pass


class Creator:

    def __init__(self, createStrategy: CreateStrategy):
        self.createStrategy = createStrategy

    def setStrategy(self, createStrategy: CreateStrategy):
        self.createStrategy = createStrategy

    def create(self, item, parent):
        self.createStrategy.create(item, parent)


class AddBookmark(CreateStrategy):

    def create(self, item: str, parent: str):
        itemList = item.split('@')
        assert len(itemList) == 2
        bookmark = BookmarkTitle(name=itemList[0], url=itemList[1], root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(bookmark)


class CreateBookmark(CreateStrategy):

    def create(self, item: str, parent: str):
        name = re.findall(r'\[.+?\]', item)[0].replace('[', '').replace(']', '')
        url = re.findall(r'\(.+?\)', item)[0].replace('[', '').replace(']', '')
        bookmark = BookmarkTitle(name=name, url=url, root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(bookmark)


class CreateBookmarkList(CreateStrategy):

    def __init__(self):
        super().__init__()
        self.createStrategy = CreateBookmark()

    def create(self, item: str, parent: str):
        if item in [' ', '']:
            return
        itemList = item.split('\n')
        for singleItem in itemList:
            self.createStrategy.create(item=singleItem, parent=parent)


class CreateTitle(CreateStrategy):

    def create(self, item: str, parent: str):
        title = BookmarkTitle(name=item, root=parent)
        singleton = Singleton.getInstance()
        singleton.addComponent(title)

