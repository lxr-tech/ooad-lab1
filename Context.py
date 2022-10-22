from Creator import *

import sys
from util import *


class OpenContext(Creator):

    def __init__(self, createStrategy: CreateStrategy):
        super().__init__(createStrategy)

    def openTitle(self, component: dict, parent: str = None):
        for name in component:
            self.setStrategy(CreateTitle())
            self.createStrategy.create(item=name, parent=parent)
            self.create(component[name], parent=name)

    def openBookmark(self, component: str, parent: str = None):
        self.setStrategy(CreateBookmarkListStrategy())
        self.createStrategy.create(item=component, parent=parent)

    def strategyMethod(self):
        Singleton.getInstance().reset()
        self.create(markdown_to_dict(sys.argv[2]), parent=None)

    def create(self, component: [dict, str], parent: str = None):
        if isinstance(component, str):
            self.openBookmark(component, parent=parent)
        else:
            self.openTitle(component, parent=parent)


class ShowContext(TreeViewer):

    def __init__(self, contentProvider: BmkContentProvider):
        super().__init__(contentProvider)

    def visitFile(self, leaf: BookmarkTitle, isLast: bool):
        suffix = '' if leaf.getReadNum() == 0 else '*'
        return super().visitFile(leaf, isLast) + suffix

    def visitDirectory(self, component: BookmarkTitle, isLast: bool):
        return super().visitDirectory(component, isLast)

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
        Singleton.getInstance().readComponent(bookmark=bookmark)


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


