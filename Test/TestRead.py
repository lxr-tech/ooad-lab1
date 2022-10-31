import io
import sys

from util import update_sys_argv
from Test.TestOpen import TestOpen


show_tree = '└── 个⼈收藏\n' \
            '    ├── 课程\n' \
            '    │   ├── elearning*\n' \
            '    │   └── ehall\n' \
            '    ├── 参考资料\n' \
            '    │   ├── 函数式\n' \
            '    │   │   └── JFP\n' \
            '    │   └── ⾯向对象\n' \
            '    └── 待阅读\n' \
            '        └── Category Theory\n'


class TestRead(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testRead(self):
        sys.stdout = io.StringIO()
        update_sys_argv(['read-bookmark', 'elearning'])
        self.invoker.read()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(show_tree, content)
