from Decorator import *


class AbstractFactory:
    def __init__(self):
        pass

    def newBookmarkVisitor(self) -> Visitor:
        return Visitor()

    def newTitleVisitor(self) -> Visitor:
        return Visitor()


class OpenFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newTitleVisitor(self) -> OpenDecorator:
        return OpenDecorator()


class ShowFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newTitleVisitor(self) -> ShowDecorator:
        return ShowDecorator()


class ListFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newTitleVisitor(self) -> ListDecorator:
        return ListDecorator()


class ReadFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newBookmarkVisitor(self) -> ReadDecorator:
        return ReadDecorator()


class AddFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newTitleVisitor(self) -> AddDecorator:
        return AddDecorator()


class DeleteFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        pass

    def newTitleVisitor(self) -> DeleteDecorator:
        return DeleteDecorator()

