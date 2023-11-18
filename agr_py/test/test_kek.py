import unittest

class Tests(unittest.TestCase):
    def test_kek(self):
        print("works")
        self.assertEqual("kek", "kek")
        
        
if __name__ == '__main__':
    unittest.main()