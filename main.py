from AppiumTest.test_appium import TestAppium
import unittest

if __name__ == "__main__":
    # load TestAppium test case.
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
