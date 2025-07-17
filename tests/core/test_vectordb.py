import unittest
from core import vectordb

class TestVectorDB(unittest.TestCase):
    def test_search_with_source(self):
        # 只测试接口可调用性
        try:
            vectordb.search_with_source("test", k=1)
        except Exception as e:
            self.fail(f"search_with_source failed: {e}")

if __name__ == "__main__":
    unittest.main()
