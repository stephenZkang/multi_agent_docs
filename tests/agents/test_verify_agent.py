from dotenv import load_dotenv
load_dotenv()
import unittest
from agents import verify_agent

class TestVerifyAgent(unittest.TestCase):
    def test_empty_input(self):
        result = verify_agent.run({"input": ""})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
