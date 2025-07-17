import unittest
from agents import qa_agent

class TestQaAgent(unittest.TestCase):
    def test_empty_input(self):
        result = qa_agent.run({"input": ""})
        self.assertIn("qa_result", result)
        self.assertIn("evidence", result)

    def test_basic_question(self):
        result = qa_agent.run({"input": "什么是AI？"})
        self.assertIn("qa_result", result)
        self.assertIn("evidence", result)

if __name__ == "__main__":
    unittest.main()
