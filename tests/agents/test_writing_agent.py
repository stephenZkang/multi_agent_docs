from dotenv import load_dotenv
load_dotenv()
import unittest
from agents import writing_agent

class TestWritingAgent(unittest.TestCase):
    def test_empty_input(self):
        result = writing_agent.run({"input": ""})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
