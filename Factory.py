from Context import *


class AbstractFactory:
    def __init__(self):
        pass

    def newContext(self) -> Context:
        return Context()


class OpenFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> OpenContext:
        return OpenContext()


class ShowFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> ShowContext:
        bmkContentProvider = BmkContentProvider()
        return ShowContext(contentProvider=bmkContentProvider)


class ListFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> ListContext:
        fsContentProvider = FSContentProvider()
        return ListContext(contentProvider=fsContentProvider)


class ReadFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> ReadContext:
        return ReadContext()


class AddFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> AddContext:
        return AddContext()


class DeleteFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newContext(self) -> DeleteContext:
        return DeleteContext()

