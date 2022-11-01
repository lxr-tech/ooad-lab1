
from Context import *


class AbstractFactory:

    def newContext(self):
        pass


class OpenFactory(AbstractFactory):

    def newContext(self) -> OpenContext:
        createStrategy = CreateTitleStrategy()
        return OpenContext(createStrategy=createStrategy)


class ShowFactory(AbstractFactory):

    def newContext(self) -> ShowContext:
        bmkContentProvider = BmkContentProvider()
        lineProvider = PrintLineProvider()
        return ShowContext(contentProvider=bmkContentProvider, lineProvider=lineProvider)


class SaveFactory(AbstractFactory):

    def newContext(self) -> SaveContext:
        bmkContentProvider = BmkContentProvider()
        lineProvider = WriteLineProvider()
        return SaveContext(contentProvider=bmkContentProvider, lineProvider=lineProvider)


class ListFactory(AbstractFactory):

    def newContext(self) -> ListContext:
        fsContentProvider = FSContentProvider()
        lineProvider = PrintLineProvider()
        return ListContext(contentProvider=fsContentProvider, lineProvider=lineProvider)


class ReadFactory(AbstractFactory):

    def newContext(self) -> ReadContext:
        return ReadContext()


class AddTitleFactory(AbstractFactory):

    def newContext(self) -> AddContext:
        createTitle = CreateTitleStrategy()
        return AddContext(createStrategy=createTitle)


class AddBookmarkFactory(AbstractFactory):

    def newContext(self) -> AddContext:
        addBookmark = AddBookmarkStrategy()
        return AddContext(createStrategy=addBookmark)


class DeleteTitleFactory(AbstractFactory):

    def newContext(self) -> DeleteContext:
        deleteBookmark = DeleteTitleStrategy()
        return DeleteContext(deleteStrategy=deleteBookmark)


class DeleteBookmarkFactory(AbstractFactory):

    def newContext(self) -> DeleteContext:
        deleteBookmark = DeleteBookmarkStrategy()
        return DeleteContext(deleteStrategy=deleteBookmark)

