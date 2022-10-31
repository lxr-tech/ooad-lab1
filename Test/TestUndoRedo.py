import io
import sys

from util import update_sys_argv
from Test.TestOpen import TestOpen

show_tree1 = '├── 个⼈收藏\n' \
             '│   ├── 课程\n' \
             '│   │   ├── elearning\n' \
             '│   │   └── ehall\n' \
             '│   ├── 参考资料\n' \
             '│   │   ├── 函数式\n' \
             '│   │   │   └── JFP\n' \
             '│   │   └── ⾯向对象\n' \
             '│   └── 待阅读\n' \
             '│       └── Category Theory\n' \
             '└── 读书笔记\n'
show_tree2 = '└── 个⼈收藏\n' \
             '    ├── 课程\n' \
             '    │   ├── elearning\n' \
             '    │   └── ehall\n' \
             '    ├── 参考资料\n' \
             '    │   ├── 函数式\n' \
             '    │   │   └── JFP\n' \
             '    │   └── ⾯向对象\n' \
             '    └── 待阅读\n' \
             '        └── Category Theory\n'


class TestUndoRedo(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testUndo(self):

        sys.stdout = io.StringIO()
        update_sys_argv(['add-title', '读书笔记'])
        self.invoker.addTitle()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(show_tree1, content)

        sys.stdout = io.StringIO()
        update_sys_argv(['undo'])
        self.invoker.undo()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(show_tree2, content)

        sys.stdout = io.StringIO()
        update_sys_argv(['redo'])
        self.invoker.redo()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(show_tree1, content)
