import unittest
from agents import weather_agent

class TestWeatherAgent(unittest.TestCase):
    def test_no_city(self):
        result = weather_agent.run({})
        self.assertIn("请提供城市名称", result["weather_result"])

    def test_invalid_city(self):
        result = weather_agent.run({"city": "不存在的城市", "weather_api_key": "demo_key"})
        self.assertIn("未能获取天气信息", result["weather_result"])

    def test_valid_city(self):
        result = weather_agent.run({"city": "北京", "weather_api_key": "demo_key"})
        self.assertTrue("天气" in result["weather_result"] or "未能获取天气信息" in result["weather_result"])

if __name__ == "__main__":
    unittest.main()
