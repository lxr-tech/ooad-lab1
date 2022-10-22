from Creator import *
from Context import *


class AbstractFactory:

    def newContext(self):
        pass


class OpenFactory(AbstractFactory):

    def newContext(self) -> OpenContext:
        createStrategy = CreateTitle()
        return OpenContext(createStrategy=createStrategy)


class ShowFactory(AbstractFactory):

    def newContext(self) -> ShowContext:
        bmkContentProvider = BmkContentProvider()
        return ShowContext(contentProvider=bmkContentProvider)


class ListFactory(AbstractFactory):

    def newContext(self) -> ListContext:
        fsContentProvider = FSContentProvider()
        return ListContext(contentProvider=fsContentProvider)


class ReadFactory(AbstractFactory):

    def newContext(self) -> ReadContext:
        return ReadContext()


class AddTitleFactory(AbstractFactory):

    def newContext(self) -> AddContext:
        createTitle = CreateTitle()
        return AddContext(createStrategy=createTitle)


class AddBookmarkFactory(AbstractFactory):

    def newContext(self) -> AddContext:
        addBookmark = AddBookmark()
        return AddContext(createStrategy=addBookmark)


class DeleteFactory(AbstractFactory):

    def newContext(self) -> DeleteContext:
        deleteBookmark = DeleteBookmark()
        return DeleteContext(deleteStrategy=deleteBookmark)

