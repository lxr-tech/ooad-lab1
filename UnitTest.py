import unittest

suite = unittest.TestLoader().discover('Test/', '*Open*')
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().discover('Test/', '*Read*')
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().discover('Test/', '*AddDelete*')
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().discover('Test/', '*UndoRedo*')
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().discover('Test/', '*Tree*')
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().discover('Test/', '*Save*')
unittest.TextTestRunner().run(suite)
