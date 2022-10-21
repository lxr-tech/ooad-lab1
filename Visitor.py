from __future__ import annotations
from abc import ABC, abstractmethod


class Component():
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

    def accept(self, visitor):
        visitor.visit(self)

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent


class Visitor:
    def __init__(self):
        pass

    def visit(self, component: Component):
        component.accept(self)


class Title(Component):
    def __init__(self, name, parent):
        super().__init__(name=name, parent=parent)

    def accept(self, visitor: Visitor):
        visitor.visit(self)

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent


class Bookmark(Component):
    def __init__(self, name, url, parent):
        super().__init__(name=name, parent=parent)
        self.readNum = 0
        self.url = url

    def accept(self, visitor: []):
        visitor.visit(self)

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addReadNum(self):
        self.readNum += 1


class Singleton:
    __instance__ = None

    def __init__(self):
        self.root = Title(name=None, parent=None)
        self.components = []

    def getRoot(self):
        return self.root

    def reset(self):
        del self.components
        self.components = []

    def addComponent(self, component: Component):
        self.components.append(component)

    def deleteComponent(self, name):
        self.components = [component for component in self.components if component.name != name]

    def getAllComponents(self):
        return [component for component in self.components if isinstance(component, Bookmark)]

    def getRoots(self):
        return [component for component in self.components if component.getParent() is None]

    def getChildren(self, parentName: str):
        return [component for component in self.components if str(component.parent).__eq__(parentName)]

    @staticmethod
    def getInstance():
        if Singleton.__instance__ is None:
            Singleton.__instance__ = Singleton()
            return Singleton.__instance__
        else:
            return Singleton.__instance__


# [python-类的前向声明]http://www.manongjc.com/detail/26-uglsentetmrdcpi.html
