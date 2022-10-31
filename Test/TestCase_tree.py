import io
import sys
import unittest

from Command import Invoker
from Controller import Controller
show_tree = '└── 个⼈收藏\n    ├── 课程\n    │   ├── elearning\n    │   └── ehall\n    ├── 参考资料\n    │   ├── 函数式\n' \
            '    │   │   └── JFP\n    │   └── ⾯向对象\n    └── 待阅读\n        └── Category Theory\n'
ls_tree = '├── .idea\n│   └── inspectionProfiles\n├── Test\n│   └── __pycache__\n├── test.bmk\n├── waste\n└── __pycache__\n'


class TestListTree(unittest.TestCase):
    def setUp(self) -> None:
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()

    def test_listTree(self):
        invoker = Invoker()
        sys.argv.extend(['ls', '-tree'])
        temp = sys.stdout
        sys.stdout = io.StringIO()
        invoker.listTree()
        content = str(sys.stdout.getvalue())
        sys.stdout = temp
        self.assertEqual(ls_tree, content)

    def tearDown(self) -> None:
        sys.argv.extend(['exit'])

class TestShowTree(unittest.TestCase):
    def setUp(self) -> None:
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()

    def test_showTree(self):
        invoker = Invoker()
        sys.argv.extend(['show', '-tree'])
        temp = sys.stdout
        sys.stdout = io.StringIO()
        invoker.showTree()
        content = str(sys.stdout.getvalue())
        sys.stdout = temp
        print(content)
        print(show_tree)
        self.assertEqual(show_tree, content)

    def tearDown(self) -> None:
        sys.argv.extend(['exit'])