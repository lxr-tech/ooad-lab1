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

    def getFullName(self) -> str:
        pass

    def isFile(self) -> bool:
        pass

    def isDirectory(self) -> bool:
        pass

    def getSiblings(self) -> List:
        pass


class FileWithPath(AbstractFile):
    def __init__(self, name: str, root: str):
        super().__init__(name=name, root=root)

    def getFullName(self) -> str:
        return self.getRoot() + '/' + self.getName()

    def isFile(self) -> bool:
        return os.path.isfile(self.getFullName())

    def isDirectory(self) -> bool:
        return os.path.isdir(self.getFullName())

    def getSiblings(self) -> List:
        return os.listdir(self.getFullName())


class ContentProvider:

    def getAllFiles(self, parent, suffix) -> List[AbstractFile]:
        pass

    def getChildren(self, parent, suffix) -> List[AbstractFile]:
        pass


class FSContentProvider(ContentProvider):

    def getAllFiles(self, parent: FileWithPath, suffix: str) -> List[FileWithPath]:
        return [FileWithPath(root=parent.getFullName(), name=name) for name in parent.getSiblings()
                if name.endswith(suffix) or FileWithPath(root=parent.getFullName(), name=name).isDirectory()]

    def getChildren(self, parent: FileWithPath, suffix: str) -> List[FileWithPath]:
        return self.getAllFiles(parent=parent, suffix=suffix) if parent.isDirectory() else []


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
            if file.isFile():
                self.list.append(self.visitFile(file, num == total - 1))
            elif file.isDirectory():
                self.list.append(self.visitDirectory(file, num == total - 1))
                self.visitAndShow(root=fileWithPath.getFullName(), name=file.getName(), suffix=suffix)
                self.space = self.space[:-4]

    def show(self, path: str, suffix: str):
        name = path.split('/')[-1]
        root = '/'.join(path.split('/')[:-1])
        self.visitAndShow(root=root, name=name, suffix=suffix)
        print(''.join(self.list))


if __name__ == '__main__':
    path = 'd:/pycharmProjects/ooad-lab1'  # 'D:/研究/论文'
    d = TreeView(contentProvider=FSContentProvider())
    d.show(path=path, suffix='.py')

