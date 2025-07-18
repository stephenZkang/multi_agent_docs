import requests

def run(input):
    city = input.get("city") or input.get("input")
    if not city:
        return {"weather_result": "请提供城市名称。"}
    try:
        api_key = input.get("weather_api_key") or "demo_key"
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={api_key}&extensions=base"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("status") == "1" and data.get("lives"):
            info = data["lives"][0]
            result = f"{info['province']}{info['city']} 天气：{info['weather']}，温度：{info['temperature']}℃，风向：{info['winddirection']}，湿度：{info['humidity']}%"
            return {"weather_result": result}
        else:
            return {"weather_result": "未能获取天气信息。"}
    except Exception as e:
        return {"weather_result": f"天气查询失败: {e}"} 