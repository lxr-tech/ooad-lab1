import io
import sys
import unittest

from Command import Invoker
from Controller import Controller


class TestSave(unittest.TestCase):
    def setUp(self) -> None:
        invoker = Invoker()
        sys.argv.extend(['open', 'test.bmk'])
        invoker.open()

    def test_save(self):
        invoker = Invoker()
#        sys.argv.extend(['add-title A'])
        sys.argv.extend(['save'])
        invoker.save()
        saveFile = open('save.bmk', 'r', encoding='utf-8')
        test_saveFile = open('Test/TestFile_save.bmk', 'r', encoding='utf-8')
        file1 = saveFile.read()
        file2 = test_saveFile.read()
        self.assertEqual(file1, file2)

    def tearDown(self) -> None:
        sys.argv.extend(['exit'])
