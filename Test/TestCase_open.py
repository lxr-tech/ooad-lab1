import unittest
import sys
sys.path.append('..')
from Component import Singleton
from Command import Invoker
from Controller import Controller
lst = [(None, '个⼈收藏'), ('个⼈收藏', '课程'), ('课程', 'elearning'), ('课程', 'ehall'), ('个⼈收藏', '参考资料'), ('参考资料', '函数式'), ('函数式', 'JFP'), ('参考资料', '⾯向对象'), ('个⼈收藏', '待阅读'), ('待阅读', 'Category Theory')]

class TestOpen(unittest.TestCase):
    def test_Open(self):
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()
        temp = [(component.getRoot(), component.getName()) for component in Singleton.__instance__.getAllComponents()]
        self.assertEqual(lst, temp)


