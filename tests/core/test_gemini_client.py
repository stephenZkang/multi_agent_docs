from dotenv import load_dotenv
load_dotenv()
import unittest
from core import gemini_client

class TestGeminiClient(unittest.TestCase):
    def test_smart_call(self):
        # 只测试接口可调用性
        try:
            gemini_client.smart_call("test prompt", "qa")
        except Exception as e:
            self.fail(f"smart_call failed: {e}")

if __name__ == "__main__":
    unittest.main()
