import unittest
import sys

loader = unittest.TestLoader()
start_dir = 'tests/'
suite = loader.discover(start_dir)

results = unittest.TextTestRunner().run(suite)

sys.exit(0 if results.failures.__len__() == 0 else 1)
