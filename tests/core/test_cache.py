import unittest
from core import cache

class TestCache(unittest.TestCase):
    def test_set_and_get(self):
        cache.set('k', 'v')
        self.assertEqual(cache.get('k'), 'v')

    def test_get_default(self):
        self.assertIsNone(cache.get('not_exist'))

if __name__ == "__main__":
    unittest.main()
