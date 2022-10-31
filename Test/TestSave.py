import io
import sys

from util import update_sys_argv
from Test.TestOpen import TestOpen


class TestSave(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testSave(self):
        update_sys_argv(['save'])
        self.invoker.save()
        saveFile = open('save.bmk', 'r', encoding='utf-8')
        testFile = open('test.bmk', 'r', encoding='utf-8')
        file1 = saveFile.read()
        file2 = testFile.read()
        self.assertEqual(file1, file2)

    def tearDown(self) -> None:
        sys.argv.extend(['exit'])
