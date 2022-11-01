
from Component import *


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


class LineProvider:
    def __init__(self):
        self.prefix = ''

    def getFileLine(self, file: Component, isLast: bool):
        pass

    def getDirectoryLine(self, directory: Component, isLast: bool):
        pass

    def prefixExtend(self, isLast: bool):
        pass

    def prefixShrink(self):
        pass


class PrintLineProvider(LineProvider):
    def __init__(self):
        super().__init__()
        self.prefix = str('')

    def getFileLine(self, file: Component, isLast: bool):
        return (self.prefix + '└── ' if isLast else self.prefix + '├── ') + file.getName()

    def getDirectoryLine(self, directory: Component, isLast: bool):
        return (self.prefix + '└── ' if isLast else self.prefix + '├── ') + directory.getName()

    def prefixExtend(self, isLast: bool):
        self.prefix = self.prefix + '    ' if isLast else str(self.prefix) + '│   '

    def prefixShrink(self):
        self.prefix = str(self.prefix[:-4])


class WriteLineProvider(LineProvider):
    def __init__(self):
        super().__init__()
        self.prefix = '# '

    def getFileLine(self, file: BookmarkTitle, isLast: bool = None):
        return '[%s](%s)' % (file.getName(), file.getUrl())

    def getDirectoryLine(self, directory: BookmarkTitle, isLast: bool = None):
        return self.prefix + directory.getName()

    def prefixExtend(self, isLast: bool = None):
        self.prefix = '#' + self.prefix

    def prefixShrink(self):
        self.prefix = self.prefix[1:]


class TreeViewer:
    def __init__(self, contentProvider: ContentProvider, lineProvider: LineProvider):
        self.contentProvider = contentProvider
        self.lineProvider = lineProvider
        self.list = []

    def visitFile(self, file: Component, isLast: bool):
        return self.lineProvider.getFileLine(file=file, isLast=isLast)

    def visitDirectory(self, directory: Component, isLast: bool):
        return self.lineProvider.getDirectoryLine(directory=directory, isLast=isLast)

    def visitAndShow(self, component: Component, suffix: str):
        files = self.contentProvider.getChildren(root=component, suffix=suffix)
        total = len(files)
        for num, file in enumerate(files):
            if self.contentProvider.isFile(file):
                self.list.append(self.visitFile(file, num == total - 1))
            elif self.contentProvider.isDirectory(file):
                self.list.append(self.visitDirectory(file, num == total - 1))
                self.lineProvider.prefixExtend(num == total - 1)
                self.visitAndShow(component=file, suffix=suffix)
                self.lineProvider.prefixShrink()
