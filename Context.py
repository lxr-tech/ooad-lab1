from Component import *

import re
from util import *


class Context:
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        pass


class OpenContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def openTitle(self, component: dict, parent: str = None):
        for name in component:
            title = BookmarkTitle(name=name, root=parent)
            singleton = Singleton.getInstance()
            singleton.addComponent(title)
            self.visitAndOpen(component[name], parent=name)

    def openBookmark(self, component: str, parent: str = None):
        if component in [' ', '']:
            return
        component = component.split('\n')
        for item in component:
            name, url = get_bmk_name_and_url(item)
            bookmark = BookmarkTitle(name=name, url=url, root=parent)
            singleton = Singleton.getInstance()
            singleton.addComponent(bookmark)

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        singleton.reset()
        self.visitAndOpen(kwargs['raw_dict'], parent=None)

    def visitAndOpen(self, component: [dict, str], parent: str = None):
        if isinstance(component, str):
            self.openBookmark(component, parent=parent)
        else:
            self.openTitle(component, parent=parent)


class ShowContext(TreeView):
    def __init__(self, contentProvider: BmkContentProvider):
        super().__init__(contentProvider)

    def visitFile(self, leaf: BookmarkTitle, isLast: bool):
        suffix = '' if leaf.getReadNum() == 0 else '*'
        return super().visitFile(leaf, isLast) + suffix

    def visitDirectory(self, component: BookmarkTitle, isLast: bool):
        return super().visitDirectory(component, isLast)

    def strategyMethod(self):
        dumpTitle = BookmarkTitle(name=None, root=None)
        self.visitAndShow(component=dumpTitle, suffix='')
        print('\n'.join(self.list))


class ListContext(TreeView):
    def __init__(self, contentProvider: FSContentProvider):
        super().__init__(contentProvider)

    def strategyMethod(self):
        name, root = get_cur_root_and_name()
        component = FileWithPath(root=root, name=name)
        self.visitAndShow(component=component, suffix='.bmk')
        print('\n'.join(self.list))


class ReadContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        bookmark = kwargs['bookmark']
        singleton = Singleton.getInstance()
        for component in singleton.getAllComponents():
            if component.name == bookmark:
                component.addReadNum()


class AddContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        if 'title' in kwargs:
            component = BookmarkTitle(name=kwargs['title'], root=kwargs['parent'])
            singleton.addComponent(component=component)
        elif 'bookmark' in kwargs:
            bookmark = kwargs['bookmark'].split('@')
            assert len(bookmark) == 2
            component = BookmarkTitle(name=bookmark[0], url=bookmark[1], root=kwargs['parent'])
            singleton.addComponent(component=component)


class DeleteContext(Context):
    def __init__(self):
        super().__init__()
        pass

    def strategyMethod(self, **kwargs):
        singleton = Singleton.getInstance()
        children = singleton.getChildren(parentName=kwargs['name'])
        for child in children:
            self.strategyMethod(name=child.getName())
        self.visitAndDelete(name=kwargs['name'])

    def visitAndDelete(self, name):
        singleton = Singleton.getInstance()
        singleton.deleteComponent(name=name)

