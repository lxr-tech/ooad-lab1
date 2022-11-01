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

