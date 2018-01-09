import unittest


def sgposit_testsuite():
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    return suite
