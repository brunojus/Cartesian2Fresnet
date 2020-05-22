import Cartesian2Fresnet
import unittest

class TestFresnet(unittest.TestCase):
    """
    Test the add function from the mymath library
    """
    def test_current_s(self):
        """
        Test the current point
        """
        result = Cartesian2Fresnet.fr.current_s
        self.assertEqual(result, 0.0)

if __name__ == '__main__':
    unittest.main()