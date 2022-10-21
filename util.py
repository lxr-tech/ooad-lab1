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


class FileWithPath:
    def __init__(self, path: str):
        self.path = path

    def getPath(self) -> str:
        return self.path

    def getName(self) -> str:
        return self.getPath().split('/')[-1]

    def isFile(self) -> bool:
        return os.path.isfile(self.getPath())

    def isDirectory(self) -> bool:
        return os.path.isdir(self.getPath())

    def getAllFiles(self, suffix: str):
        return [FileWithPath(self.getPath() + '/' + name) for name in os.listdir(self.getPath())
                if name.endswith(suffix) or FileWithPath(self.getPath() + '/' + name).isDirectory()]


class FSNameProvider:

    def getName(self, fileWithPath: FileWithPath) -> str:
        return fileWithPath.getName()


class FSContentProvider:
    def __init__(self, root: FileWithPath):
        self.root = root

    def getRoots(self, suffix: str) -> List[FileWithPath]:
        return self.root.getAllFiles(suffix)

    def getChildren(self, suffix: str, parent: FileWithPath) -> List[FileWithPath]:
        return parent.getAllFiles(suffix) if parent.isDirectory() else []


class TreeView(object):
    def __init__(self, contentProvider: FSContentProvider, nameProvider: FSNameProvider):
        self.contentProvider = contentProvider
        self.nameProvider = nameProvider
        self.space = ''
        self.list = []

    def visitLeaf(self, leaf, isLast):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        self.list.append(prefix + self.nameProvider.getName(leaf) + "\n")

    def visitComponent(self, component, isLast):
        prefix = str(self.space) + '└── ' if isLast else str(self.space) + '├── '
        self.list.append(prefix + self.nameProvider.getName(component) + "\n")
        self.space = str(self.space) + '    ' if isLast else str(self.space) + '│   '

    def visitAndShow(self, path: str, suffix: str):
        fileWithPath = FileWithPath(path=path)
        files = self.contentProvider.getChildren(parent=fileWithPath, suffix=suffix)
        total = len(files)
        for num, file in enumerate(files):
            if file.isFile():
                self.visitLeaf(file, num == total-1)
            elif file.isDirectory():
                self.visitComponent(file, num == total-1)
                self.visitAndShow(fileWithPath.getPath() + '/' + self.nameProvider.getName(file), suffix=suffix)
                self.space = self.space[:-4]
        return self.list

    def show(self, path: str, suffix: str):
        self.visitAndShow(path=path, suffix=suffix)
        print(''.join(self.list))


if __name__ == '__main__':
    path = 'd:/pycharmProjects/ooad-lab1'  # 'D:/研究/论文'
    fsContentProvider = FSContentProvider(root=FileWithPath(path=path))
    fsNameProvider = FSNameProvider()
    d = TreeView(contentProvider=fsContentProvider, nameProvider=fsNameProvider)
    d.show(path=path, suffix='.py')

