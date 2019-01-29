import unittest
import sys

loader = unittest.TestLoader()
start_dir = 'tests/'
suite = loader.discover(start_dir)

results = unittest.TextTestRunner().run(suite)

sys.exit(results.failures.__len__() + results.errors.__len__())
