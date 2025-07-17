import unittest
from agents import pdf_agent

class TestPdfAgent(unittest.TestCase):
    def test_no_input(self):
        result = pdf_agent.run({})
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
