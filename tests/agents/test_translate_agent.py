import unittest
from agents import translate_agent

class TestTranslateAgent(unittest.TestCase):
    def test_empty_input(self):
        result = translate_agent.run({"input": ""})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
