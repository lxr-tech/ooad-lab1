import os
from typing import List


class Component:

    def __init__(self, name: str = None, root: str = None):
        self.name = name
        self.root = root

    def getRoot(self) -> str:
        return self.root

    def getName(self) -> str:
        return self.name

    def getFullName(self) -> str:
        pass


class FileWithPath(Component):

    def __init__(self, name: str = None, root: str = None):
        super().__init__(name=name, root=root)

    def getFullName(self) -> str:
        return self.getRoot() + '/' + self.getName()


class BookmarkTitle(Component):

    def __init__(self, name: str = None, root: str = None, **kwargs):
        super().__init__(name=name, root=root)
        self.url = kwargs['url'] if 'url' in kwargs else None
        self.readNum = 0

    def getFullName(self) -> str:
        return self.name

    def getUrl(self) -> str:
        return self.url

    def getReadNum(self):
        return self.readNum

    def addReadNum(self):
        self.readNum += 1


class ContentProvider:

    def isFile(self, component: Component) -> bool:
        pass

    def isDirectory(self, component: Component) -> bool:
        pass

    def getSiblings(self, component: Component) -> List:
        pass

    def getAllFiles(self, root: Component, suffix: str) -> List[Component]:
        pass

    def getChildren(self, root: Component, suffix: str) -> List[Component]:
        pass

    def provideType(self) -> str:
        pass


class FSContentProvider(ContentProvider):

    def isFile(self, component: FileWithPath) -> bool:
        return os.path.isfile(component.getFullName())

    def isDirectory(self, component: FileWithPath) -> bool:
        return os.path.isdir(component.getFullName())

    def getSiblings(self, component: FileWithPath) -> List:
        return os.listdir(component.getFullName())

    def getAllFiles(self, root: FileWithPath, suffix: str) -> List[FileWithPath]:
        return [FileWithPath(root=root.getFullName(), name=name) for name in self.getSiblings(root)
                if name.endswith(suffix) or self.isDirectory(FileWithPath(root=root.getFullName(), name=name))]

    def getChildren(self, root: FileWithPath, suffix: str) -> List[FileWithPath]:
        return self.getAllFiles(root=root, suffix=suffix) if self.isDirectory(root) else []

    def provideType(self) -> str:
        return 'FileWithPath'


class Singleton:
    __instance__ = None

    def __init__(self):
        self.components = []

    def reset(self):
        del self.components
        self.components = []

    def getAllComponents(self):
        return self.components

    def addComponent(self, component: BookmarkTitle):
        self.components.append(component)

    def readComponent(self, bookmarkName: str):
        for component in self.getAllComponents():
            if component.name == bookmarkName:
                component.addReadNum()

    def deleteComponent(self, name: str):
        self.components = [component for component in self.components if component.name != name]

    def getChildren(self, parentName: str):
        return [component for component in self.components if component.getRoot() == parentName]

    @staticmethod
    def getInstance():
        if Singleton.__instance__ is None:
            Singleton.__instance__ = Singleton()
            return Singleton.__instance__
        else:
            return Singleton.__instance__


class BmkContentProvider(ContentProvider):

    def isFile(self, component: BookmarkTitle) -> bool:
        return component.url is not None

    def isDirectory(self, component: BookmarkTitle) -> bool:
        return component.url is None

    def getSiblings(self, component: BookmarkTitle) -> List:
        singleton = Singleton.getInstance()
        return singleton.getChildren(parentName=component.getRoot())

    def getAllFiles(self, root: BookmarkTitle, suffix: str) -> List[BookmarkTitle]:
        return [component for component in self.getSiblings(root)
                if component.getName().endswith(suffix) or self.isDirectory(component)]

    def getChildren(self, root: BookmarkTitle, suffix: str) -> List[BookmarkTitle]:
        singleton = Singleton.getInstance()
        return singleton.getChildren(parentName=root.getName())

    def provideType(self) -> str:
        return 'BookmarkTitle'


class TreeViewer(object):
    def __init__(self, contentProvider: ContentProvider):
        self.contentProvider = contentProvider
        self.space = ''
        self.list = []

    def visitFile(self, file: Component, isLast: bool):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        return prefix + file.getName()

    def visitDirectory(self, directory: Component, isLast: bool):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        self.space = str(self.space) + '    ' if isLast else str(self.space) + '│   '
        return prefix + directory.getName()

    def visitAndShow(self, component: Component, suffix: str):
        files = self.contentProvider.getChildren(root=component, suffix=suffix)
        total = len(files)
        for num, file in enumerate(files):
            if self.contentProvider.isFile(file):
                self.list.append(self.visitFile(file, num == total - 1))
            elif self.contentProvider.isDirectory(file):
                self.list.append(self.visitDirectory(file, num == total - 1))
                self.visitAndShow(component=file, suffix=suffix)
                self.space = self.space[:-4]


class TreeSaver(object):
    def __init__(self, contentProvider: BmkContentProvider):
        self.contentProvider = contentProvider
        self.space = ' '
        self.list = []

    def visitFile(self, file: BookmarkTitle):
        return '[%s](%s)' % (file.getName(), file.getUrl())

    def visitDirectory(self, directory: BookmarkTitle):
        self.space = '#' + self.space
        return self.space + directory.getName()

    def visitAndShow(self, component: BookmarkTitle, suffix: str):
        files = self.contentProvider.getChildren(root=component, suffix=suffix)
        for num, file in enumerate(files):
            if self.contentProvider.isFile(file):
                self.list.append(self.visitFile(file))
            elif self.contentProvider.isDirectory(file):
                self.list.append(self.visitDirectory(file))
                self.visitAndShow(component=file, suffix=suffix)
                self.space = self.space[1:]
