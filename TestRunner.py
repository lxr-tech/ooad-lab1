import unittest
from HTMLTestRunner import HTMLTestRunner

suite = unittest.defaultTestLoader.discover('./Case', '*add*') #测试的test case位置： 目录  文件名
file = './report.html'
with open(file, 'wb') as f:
    runner = HTMLTestRunner(f)
    runner.run(suite)
