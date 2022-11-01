import io
import sys

from util import update_sys_argv
from Test.TestOpen import TestOpen

showTreeValid = '└── 个⼈收藏\n' \
                '    ├── 课程\n' \
                '    │   ├── elearning\n' \
                '    │   └── ehall\n' \
                '    ├── 参考资料\n' \
                '    │   ├── 函数式\n' \
                '    │   │   └── JFP\n' \
                '    │   └── ⾯向对象\n' \
                '    └── 待阅读\n' \
                '        └── Category Theory\n'
listTreeValid = '├── test.bmk\n' \
                '├── save.bmk\n' \
                '├── Test\n' \
                '│   └── __pycache__\n' \
                '└── __pycache__\n'


class TestShowTree(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testShowTree(self):

        sys.stdout = io.StringIO()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(showTreeValid, content)

    def tearDown(self) -> None:
        update_sys_argv(['exit'])


class TestListTree(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testListTree(self):

        sys.stdout = io.StringIO()
        update_sys_argv(['ls-tree'])
        self.invoker.listTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(listTreeValid, content)

    def tearDown(self) -> None:
        update_sys_argv(['exit'])
