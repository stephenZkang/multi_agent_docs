import unittest
from core import logger

class TestLogger(unittest.TestCase):
    def test_logger_info(self):
        try:
            logger.info("test info log")
        except Exception as e:
            self.fail(f"Logger info failed: {e}")

if __name__ == "__main__":
    unittest.main()
