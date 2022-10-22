from Strategy import *

import sys
from util import *


class OpenContext(Creator):

    def __init__(self, createStrategy: CreateStrategy):
        super().__init__(createStrategy)

    def openTitle(self, item: dict, parent: str = None):
        for name in item:
            self.setStrategy(CreateTitle())
            self.createStrategy.create(item=name, parent=parent)
            self.create(item[name], parent=name)

    def openBookmark(self, item: str, parent: str = None):
        self.setStrategy(CreateBookmarkListStrategy())
        self.createStrategy.create(item=item, parent=parent)

    def strategyMethod(self):
        Singleton.getInstance().reset()
        self.create(markdown_to_dict(sys.argv[2]), parent=None)

    def create(self, item: [dict, str], parent: str = None):
        if isinstance(item, str):
            self.openBookmark(item, parent=parent)
        else:
            self.openTitle(item, parent=parent)


class ShowContext(TreeViewer):

    def __init__(self, contentProvider: BmkContentProvider):
        super().__init__(contentProvider)

    def visitFile(self, file: BookmarkTitle, isLast: bool):
        suffix = '' if file.getReadNum() == 0 else '*'
        return super().visitFile(file, isLast) + suffix

    def visitDirectory(self, directory: BookmarkTitle, isLast: bool):
        return super().visitDirectory(directory, isLast)

    def strategyMethod(self):
        dumpTitle = BookmarkTitle(name=None, root=None)
        self.visitAndShow(component=dumpTitle, suffix='')
        print('\n'.join(self.list))


class ListContext(TreeViewer):

    def __init__(self, contentProvider: FSContentProvider):
        super().__init__(contentProvider)

    def strategyMethod(self):
        name, root = get_cur_root_and_name()
        component = FileWithPath(root=root, name=name)
        self.visitAndShow(component=component, suffix='.bmk')
        print('\n'.join(self.list))


class ReadContext:

    def strategyMethod(self, bookmark):
        Singleton.getInstance().readComponent(bookmarkName=bookmark)


class AddContext(Creator):

    def __init__(self, createStrategy: CreateStrategy):
        super().__init__(createStrategy)

    def strategyMethod(self, item, parent):
        self.createStrategy.create(item=item, parent=parent)


class DeleteContext(Deleter):

    def __init__(self, deleteStrategy: DeleteStrategy):
        super().__init__(deleteStrategy)

    def strategyMethod(self, item):
        self.deleteStrategy.delete(item=item)


