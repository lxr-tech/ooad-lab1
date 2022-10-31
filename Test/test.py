import unittest

suite = unittest.TestLoader().discover('./', '*add*')
unittest.TextTestRunner().run(suite)