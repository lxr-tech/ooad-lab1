import io
import sys
import unittest

from Command import Invoker
from Controller import Controller
show_tree1 = '├── 个⼈收藏\n│   ├── 课程\n│   │   ├── elearning\n│   │   └── ehall\n│   ├── 参考资料\n│   │   ├── 函数式\n│' \
            '   │   │   └── JFP\n│   │   └── ⾯向对象\n│   └── 待阅读\n│       └── Category Theory\n└── 读书笔记\n'
show_tree2 = '└── 个⼈收藏\n    ├── 课程\n    │   ├── elearning\n    │   └── ehall\n    ├── 参考资料\n    │   ├── 函数式\n' \
            '    │   │   └── JFP\n    │   └── ⾯向对象\n    └── 待阅读\n        └── Category Theory\n'
class TestAddTitle(unittest.TestCase):
    # def setUp(self) -> None:
    #     invoker = Invoker()
    #     sys.argv.extend(['open', 'test.bmk'])
    #     invoker.open()

    def test_addTitle(self):
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['add-title', '读书笔记'])
        invoker.addTitle()
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['show-tree'])
        temp = sys.stdout
        sys.stdout = io.StringIO()
        invoker.showTree()
        content = str(sys.stdout.getvalue())
        sys.stdout = temp
        print(content)
        print(show_tree1)
        self.assertEqual(show_tree1, content)

    def test_delTitle(self):
        invoker = Invoker()
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['delete-title', '读书笔记'])
        invoker.deleteTitle()
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['show-tree'])
        temp = sys.stdout
        sys.stdout = io.StringIO()
        invoker.showTree()
        content = str(sys.stdout.getvalue())
        sys.stdout = temp
        print(content)
        print(show_tree2)
        self.assertEqual(show_tree2, content)

    # def tearDown(self) -> None:
    #     sys.argv.extend(['exit'])