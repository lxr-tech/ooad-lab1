import unittest
import sys
import io
sys.path.append('..')
from Component import Singleton
from Command import Invoker
from Controller import Controller
lst = [(None, '个⼈收藏'), ('个⼈收藏', '课程'), ('课程', 'elearning*'), ('课程', 'ehall'), ('个⼈收藏', '参考资料'), ('参考资料', '函数式'), ('函数式', 'JFP'), ('参考资料', '⾯向对象'), ('个⼈收藏', '待阅读'), ('待阅读', 'Category Theory')]
show_tree = '└── 个⼈收藏\n\
    ├── 课程\n\
    │   ├── elearning*\n\
    │   └── ehall\n\
    ├── 参考资料\n\
    │   ├── 函数式\n\
    │   │   └── JFP\n\
    │   └── ⾯向对象\n\
    └── 待阅读\n\
        └── Category Theory\n'
class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()
        sys.argv = [sys.argv[0]]

    def test_read(self):
        invoker = Invoker()
        sys.argv.extend(['read-bookmark', 'elearning'])
        invoker.read()
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['show-tree'])
        temp = sys.stdout
        sys.stdout = io.StringIO()
        invoker.showTree()
        content = str(sys.stdout.getvalue())
        sys.stdout = temp
        # print(content)
        # print(show_tree)
        self.assertEqual(show_tree, content)

    def tearDown(self) -> None:
        sys.argv.extend(['exit'])