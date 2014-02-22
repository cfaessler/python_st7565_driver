import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('./test', pattern='*tests.py')
    unittest.TextTestRunner(verbosity=2).run(suite)