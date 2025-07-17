import unittest
from agents import summary_agent

class TestSummaryAgent(unittest.TestCase):
    def test_empty_input(self):
        result = summary_agent.run({"input": ""})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
