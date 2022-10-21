from Visitor import *

import re, os
from util import *


class Decorator(Visitor):
    def __init__(self):
        super().__init__()
        self.visitor = Visitor()
        pass

    def visit(self, component: Component, **kwargs):
        pass


class OpenDecorator(Decorator):
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

    def visit(self, component: Component, **kwargs):
        singleton = Singleton.getInstance()
        singleton.reset()
        self.visitAndOpen(kwargs['raw_dict'], parent=None)

    def visitAndOpen(self, component: [dict, str], parent: str = None):
        if isinstance(component, str):
            self.openBookmark(component, parent=parent)
        else:
            self.openTitle(component, parent=parent)


class ShowDecorator(Decorator):
    def __init__(self):
        super().__init__()
        self.space = ''
        self.list = []

    def visit(self, component: Component, **kwargs):
        singleton = Singleton.getInstance()
        total = len(singleton.getRoots())
        print(len(singleton.components))
        for num, component in enumerate(singleton.getRoots()):
            self.visitTitle(component, num == total-1)
            self.visitAndShow(component)
            self.space = self.space[:-4]
        print(''.join(self.list), end='')

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


class ListDecorator(Decorator):  # 无法去除内部没有.bmk的文件夹
    def __init__(self):
        super().__init__()
        pass

    def visit(self, component: Component, **kwargs):
        self.visitAndList(os.getcwd())

    def visitAndList(self, path: str):
        contentProvider = FSContentProvider(root=FileWithPath(path=path))
        nameProvider = FSNameProvider()
        treeView = TreeView(contentProvider=contentProvider, nameProvider=nameProvider)
        treeView.show(path=path, suffix='.bmk')


class ReadDecorator(Decorator):
    def __init__(self):
        super().__init__()
        pass

    def visit(self, component: Component, **kwargs):
        self.visitAndRead(bookmark=kwargs['bookmark'])

    def visitAndRead(self, bookmark: str):
        singleton = Singleton.getInstance()
        for component in singleton.getAllComponents():
            if component.name == bookmark:
                component.addReadNum()


class AddDecorator(Decorator):
    def __init__(self):
        super().__init__()
        pass

    def visit(self, component: Component, **kwargs):
        if 'title' in kwargs:
            component = Title(name=kwargs['title'], parent=kwargs['parent'])
            self.visitAndAdd(component)
        elif 'bookmark' in kwargs:
            bookmark = kwargs['bookmark'].split('@')
            assert len(bookmark) == 2
            component = Bookmark(name=bookmark[0], url=bookmark[1], parent=kwargs['parent'])
            self.visitAndAdd(component)

    def visitAndAdd(self, component):
        singleton = Singleton.getInstance()
        singleton.addComponent(component=component)


class DeleteDecorator(Decorator):
    def __init__(self):
        super().__init__()
        pass

    def visit(self, component: Component, **kwargs):
        singleton = Singleton.getInstance()
        children = singleton.getChildren(parentName=kwargs['name'])
        for child in children:
            self.visit(component=component, name=child.getName())
        self.visitAndDelete(name=kwargs['name'])

    def visitAndDelete(self, name):
        singleton = Singleton.getInstance()
        singleton.deleteComponent(name=name)


# class OpenTitle(OpenDecorator):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Title, **kwargs):
#         raw_dict = kwargs['raw_dict']
#         print('open title', raw_dict)
#         process(component=raw_dict, parent=component)
#
#
# class ShowBookmark(ShowDecorator):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Bookmark, **kwargs):
#         singleton = Singleton.getInstance()
#         current, depth = singleton.getCurrent()
#         print(' ' * depth, component.name, component.url)
#
#     def show(self, component: Bookmark):
#         pass
#
#
# class ShowTitle(ShowDecorator):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Title, **kwargs):
#         singleton = Singleton.getInstance()
#         current, depth = singleton.getCurrent()
#         print(''.join([' '] * depth), component.name)
#         for child in component.getChildren():
#             singleton.setCurrent(current=child, depth=depth+1)
#             Visitor().visit(component=child)
#         singleton.setCurrent(current=component, depth=depth)
#
#     def show(self, component: Title):
#         pass
#
#
# class AddBookmark(Visitor):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Component, **kwargs):
#         pass
#
#     def add(self, component: Component):
#         pass
#
#
# class AddTitle(Visitor):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Component, **kwargs):
#         pass
#
#     def add(self, component: Component):
#         pass
#
#
# class DeleteBookmark(Visitor):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Component, **kwargs):
#         pass
#
#     def delete(self, component: Component):
#         pass
#
#
# class DeleteTitle(Visitor):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Component, **kwargs):
#         pass
#
#     def delete(self, component: Component):
#         pass
#
#
# class ReadBookmark(Visitor):
#     def __init__(self):
#         super().__init__()
#         pass
#
#     def visit(self, component: Component, **kwargs):
#         pass
#
#     def read(self, component: Component):
#         pass
#
