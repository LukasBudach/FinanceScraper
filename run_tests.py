import unittest

loader = unittest.TestLoader()
start_dir = 'tests/'
suite = loader.discover(start_dir)

unittest.TextTestRunner().run(suite)
