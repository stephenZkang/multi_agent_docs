import unittest
from agents import search_agent

class TestSearchAgent(unittest.TestCase):
    def test_empty_query(self):
        result = search_agent.run({"input": ""})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
