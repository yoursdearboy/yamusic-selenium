import unittest

def make_suite(clazz, maker):
  suite = unittest.TestSuite()
  testloader = unittest.TestLoader()
  testnames = testloader.getTestCaseNames(clazz)
  for name in testnames:
    for test in maker(name):
      suite.addTest(test)
  return suite
