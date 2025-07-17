from dotenv import load_dotenv
load_dotenv()
import unittest
from agents import qa_agent

class TestQaAgent(unittest.TestCase):
    def test_empty_input(self):
        question = ""
        result = qa_agent.run({"input": question})
        print(f"问题: {question}")
        print(f"答案: {result.get('qa_result')}")
        self.assertIn("qa_result", result)
        self.assertIn("evidence", result)

    def test_basic_question(self):
        question = "什么是AI？"
        result = qa_agent.run({"input": question})
        print(f"问题: {question}")
        print(f"答案: {result.get('qa_result')}")
        self.assertIn("qa_result", result)
        self.assertIn("evidence", result)

if __name__ == "__main__":
    unittest.main()
