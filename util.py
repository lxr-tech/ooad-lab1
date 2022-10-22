import os
import json
from typing import List

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester


def markdown_to_dict(markdown_file):
    nester = CMarkASTNester()
    renderer = Renderer()
    f = open(markdown_file, 'r', encoding='UTF-8', errors='ignore')
    ast = CommonMark.DocParser().parse(f.read())
    f.close()
    nested = nester.nest(ast)
    rendered = renderer.stringify_dict(nested)
    rendered = json.loads(json.dumps(rendered))
    return rendered


def every(lst, fn=lambda x: x):
    return all(map(fn, lst))


class AbstractFile:

    def __init__(self, name: str, root: str):
        self.name = name
        self.root = root

    def getRoot(self) -> str:
        return self.root

    def getName(self) -> str:
        return self.name


class FileWithPath(AbstractFile):
    def __init__(self, name: str, root: str):
        super().__init__(name=name, root=root)

    def getFullName(self) -> str:
        return self.getRoot() + '/' + self.getName()

#
# class BookmarkTitle(AbstractFile):
#     def __init__(self, name: str, root: str, **kwargs):
#         super().__init__(name=name, root=root)
#         self.url = kwargs['url'] if 'url' in kwargs else None
#         self.readNum = 0
#
#     def addReadNum(self):
#         self.readNum += 1
#

class ContentProvider:

    def isFile(self, abstractFile: AbstractFile) -> bool:
        pass

    def isDirectory(self, abstractFile: AbstractFile) -> bool:
        pass

    def getSiblings(self, abstractFile: AbstractFile) -> List:
        pass

    def getAllFiles(self, parent: AbstractFile, suffix: str) -> List[AbstractFile]:
        pass

    def getChildren(self, parent: AbstractFile, suffix: str) -> List[AbstractFile]:
        pass


class FSContentProvider(ContentProvider):

    def isFile(self, abstractFile: FileWithPath) -> bool:
        return os.path.isfile(abstractFile.getFullName())

    def isDirectory(self, abstractFile: FileWithPath) -> bool:
        return os.path.isdir(abstractFile.getFullName())

    def getSiblings(self, abstractFile: FileWithPath) -> List:
        return os.listdir(abstractFile.getFullName())

    def getAllFiles(self, parent: FileWithPath, suffix: str) -> List[FileWithPath]:
        return [FileWithPath(root=parent.getFullName(), name=name) for name in self.getSiblings(parent)
                if name.endswith(suffix) or self.isDirectory(FileWithPath(root=parent.getFullName(), name=name))]

    def getChildren(self, parent: FileWithPath, suffix: str) -> List[FileWithPath]:
        return self.getAllFiles(parent=parent, suffix=suffix) if self.isDirectory(parent) else []

#
# class Singleton:
#     __instance__ = None
#
#     def __init__(self):
#         self.components = []
#
#     def reset(self):
#         del self.components
#         self.components = []
#
#     def addComponent(self, component: BookmarkTitle):
#         self.components.append(component)
#
#     def deleteComponent(self, name):
#         self.components = [component for component in self.components if component.name != name]
#     #
#     # def getAllComponents(self):
#     #     return [component for component in self.components if isinstance(component, Bookmark)]
#
#     def getChildren(self, parentName: str):
#         return [component for component in self.components if str(component.getRoot()).__eq__(parentName)]
#     #
#     # def getRoots(self):
#     #     return [component for component in self.components if component.getRoot() is None]
#
#     @staticmethod
#     def getInstance():
#         if Singleton.__instance__ is None:
#             Singleton.__instance__ = Singleton()
#             return Singleton.__instance__
#         else:
#             return Singleton.__instance__
#
#
# class BmkContentProvider(ContentProvider):
#
#     def isFile(self, abstractFile: BookmarkTitle) -> bool:
#         return abstractFile.url is not None
#
#     def isDirectory(self, abstractFile: BookmarkTitle) -> bool:
#         return abstractFile.url is None
#
#     def getSiblings(self, abstractFile: BookmarkTitle) -> List:
#         singleton = Singleton.getInstance()
#         return singleton.getChildren(parentName=abstractFile.getRoot())
#
#     def getAllFiles(self, parent: BookmarkTitle, suffix: str) -> List[BookmarkTitle]:
#         return [BookmarkTitle(root=parent.getRoot(), name=name) for name in self.getSiblings(parent)
#                 if name.endswith(suffix) or self.isDirectory(BookmarkTitle(root=parent.getRoot(), name=name))]
#
#     def getChildren(self, parent: BookmarkTitle, suffix: str) -> List[BookmarkTitle]:
#         return self.getAllFiles(parent=parent, suffix=suffix) if self.isDirectory(parent) else []
#

class TreeView(object):
    def __init__(self, contentProvider: ContentProvider):
        self.contentProvider = contentProvider
        self.space = ''
        self.list = []

    def visitFile(self, leaf, isLast):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        return prefix + leaf.getName() + "\n"

    def visitDirectory(self, component, isLast):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        self.space = str(self.space) + '    ' if isLast else str(self.space) + '│   '
        return prefix + component.getName() + "\n"

    def visitAndShow(self, root: str, name: str, suffix: str):
        fileWithPath = FileWithPath(root=root, name=name)
        files = self.contentProvider.getChildren(parent=fileWithPath, suffix=suffix)
        total = len(files)
        for num, file in enumerate(files):
            if self.contentProvider.isFile(file):
                self.list.append(self.visitFile(file, num == total - 1))
            elif self.contentProvider.isDirectory(file):
                self.list.append(self.visitDirectory(file, num == total - 1))
                self.visitAndShow(root=fileWithPath.getFullName(), name=file.getName(), suffix=suffix)
                self.space = self.space[:-4]

    def show(self, path: str, suffix: str):
        name = path.split('/')[-1]
        root = '/'.join(path.split('/')[:-1])
        self.visitAndShow(root=root, name=name, suffix=suffix)
        print(''.join(self.list), end='')


if __name__ == '__main__':
    path = 'd:/pycharmProjects/ooad-lab1'  # 'D:/研究/论文'
    d = TreeView(contentProvider=FSContentProvider())
    d.show(path=path, suffix='.py')

