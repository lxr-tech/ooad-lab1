
class Component:
    def __init__(self, name=None, root=None):
        self.name = name
        self.root = root

    def getName(self):
        return self.name

    def getRoot(self):
        return self.root


class Title(Component):
    def __init__(self, name, root):
        super().__init__(name=name, root=root)

    def getName(self):
        return self.name

    def getRoot(self):
        return self.root


class Bookmark(Component):
    def __init__(self, name, url, root):
        super().__init__(name=name, root=root)
        self.readNum = 0
        self.url = url

    def getName(self):
        return self.name

    def getRoot(self):
        return self.root

    def addReadNum(self):
        self.readNum += 1


class Singleton:
    __instance__ = None

    def __init__(self):
        self.root = Title(name=None, root=None)
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
        return [component for component in self.components if component.getRoot() is None]

    def getChildren(self, parentName: str):
        return [component for component in self.components if str(component.getRoot()).__eq__(parentName)]

    @staticmethod
    def getInstance():
        if Singleton.__instance__ is None:
            Singleton.__instance__ = Singleton()
            return Singleton.__instance__
        else:
            return Singleton.__instance__


# [python-类的前向声明]http://www.manongjc.com/detail/26-uglsentetmrdcpi.html
