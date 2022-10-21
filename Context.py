from Component import *

import re, os
from util import *


class Context:
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        pass


class OpenContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def openTitle(self, component: dict, parent: str = None):
        for name in component:
            title = Title(name=name, parent=parent)
            singleton = Singleton.getInstance()
            singleton.addComponent(title)
            self.visitAndOpen(component[name], parent=name)

    def openBookmark(self, component: str, parent: str = None):
        if component in [' ', '']:
            return
        component = component.split('\n')
        for item in component:
            name = re.findall(r'\[.+?\]', item)[0].replace('[', '').replace(']', '')
            url = re.findall(r'\(.+?\)', item)[0].replace('[', '').replace(']', '')
            bookmark = Bookmark(name=name, url=url, parent=parent)
            singleton = Singleton.getInstance()
            singleton.addComponent(bookmark)

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        singleton.reset()
        self.visitAndOpen(kwargs['raw_dict'], parent=None)

    def visitAndOpen(self, component: [dict, str], parent: str = None):
        if isinstance(component, str):
            self.openBookmark(component, parent=parent)
        else:
            self.openTitle(component, parent=parent)


class ShowContext(Context):
    def __init__(self):
        super().__init__()
        self.space = ''
        self.list = []

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        total = len(singleton.getRoots())
        print(len(singleton.components))
        for num, component in enumerate(singleton.getRoots()):
            self.visitTitle(component, num == total-1)
            self.visitAndShow(component)
            self.space = self.space[:-4]
        return self.list

    def visitAndShow(self, component: Component):
        singleton = Singleton.getInstance()
        components = singleton.getChildren(component.getName())
        total = len(components)
        for num, component in enumerate(components):
            if isinstance(component, Bookmark):
                self.visitBookmark(component, num == total-1)
            else:
                self.visitTitle(component, num == total-1)
                self.visitAndShow(component)
                self.space = self.space[:-4]
        return self.list

    def visitBookmark(self, bookmark: Bookmark, isLast: bool):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        suffix = '' if bookmark.readNum == 0 else '*'
        self.list.append(prefix + bookmark.getName() + suffix + "\n")

    def visitTitle(self, title: Title, isLast: bool):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        self.list.append(prefix + title.getName() + "\n")
        self.space = str(self.space) + '    ' if isLast else str(self.space) + '│   '


class ListContext(Context):  # 无法去除内部没有.bmk的文件夹
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        path = os.getcwd()
        contentProvider = ContentProvider(root=AbstractFile(path=path))
        treeView = TreeView(contentProvider=contentProvider)
        treeView.show(path=path, suffix='.bmk')


class ReadContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        bookmark = kwargs['bookmark']
        singleton = Singleton.getInstance()
        for component in singleton.getAllComponents():
            if component.name == bookmark:
                component.addReadNum()


class AddContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        if 'title' in kwargs:
            component = Title(name=kwargs['title'], parent=kwargs['parent'])
            singleton.addComponent(component=component)
        elif 'bookmark' in kwargs:
            bookmark = kwargs['bookmark'].split('@')
            assert len(bookmark) == 2
            component = Bookmark(name=bookmark[0], url=bookmark[1], parent=kwargs['parent'])
            singleton.addComponent(component=component)


class DeleteContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        children = singleton.getChildren(parentName=kwargs['name'])
        for child in children:
            self.strategyMethod(name=child.getName())
        self.visitAndDelete(name=kwargs['name'])

    def visitAndDelete(self, name):
        singleton = Singleton.getInstance()
        singleton.deleteComponent(name=name)

