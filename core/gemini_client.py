

import os
import random
import time
import requests

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
except ImportError:
    pipeline = None
    AutoTokenizer = None
    AutoModelForCausalLM = None

class GeminiClient:
    def call_local(self, prompt, model_name_or_path=None):
        # 本地开源大模型推理，需安装 transformers
        if pipeline is None:
            raise ImportError("请先 pip install transformers")
        model_name_or_path = model_name_or_path or os.environ.get("LOCAL_LLM", "Qwen/Qwen1.5-0.5B-Chat")
        pipe = pipeline("text-generation", model=model_name_or_path, tokenizer=model_name_or_path, device_map="auto")
        # 兼容不同模型的输入格式
        messages = [
            {"role": "user", "content": prompt}
        ]
        # 只取第一个结果
        result = pipe(prompt, max_new_tokens=512, do_sample=True)
        return result[0]["generated_text"].strip() if isinstance(result, list) else str(result)
    def __init__(self, provider=None):
        # provider: 'openai', 'gemini', 'ernie', 'mock'，可通过环境变量或参数指定
        self.provider = provider or os.environ.get("LLM_PROVIDER", "mock")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.ernie_api_key = os.environ.get("ERNIE_API_KEY", "")

    def call_openai(self, prompt, model="gpt-3.5-turbo"):
        try:
            import openai
        except ImportError:
            raise ImportError("请先 pip install openai")
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def call_gemini(self, prompt, model="models/gemini-2.0-flash"):
        """
        使用 Google Gemini 大模型进行推理。
        默认模型为 models/gemini-2.0-flash，可根据实际可用模型名调整。
        """
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("请先 pip install google-generativeai")
        genai.configure(api_key=self.gemini_api_key)
        print("调用模型:", model)
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text.strip()

    def call_ernie(self, prompt, model="ernie-bot-turbo"):
        # 百度 ERNIE Bot API
        # 你需要先获取 access_token
        access_token = self.ernie_api_key
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}?access_token={access_token}"
        headers = {"Content-Type": "application/json"}
        data = {"messages": [{"role": "user", "content": prompt}]}
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", "")

    def call_mock(self, prompt: str, model="mock") -> str:
        time.sleep(0.2)
        responses = {
            "writing": "这是根据总结生成的商业介绍文本。",
            "translate": "This is the translated English text.",
            "verify": "内容符合ESG可持续发展原则，无明显问题。",
            "qa": "根据文档内容，Web3 将推动绿色能源的发展。",
            "vision": "图像内容识别结果。"
        }
        for key in responses:
            if key in prompt or key == model:
                return responses[key]
        return random.choice(list(responses.values()))

    def smart_call(self, prompt: str, task_type: str, provider=None) -> str:
        provider = provider or self.provider
        if provider == "openai":
            return self.call_openai(prompt)
        elif provider == "gemini":
            return self.call_gemini(prompt)
        elif provider == "ernie":
            return self.call_ernie(prompt)
        elif provider == "local":
            return self.call_local(prompt)
        else:
            return self.call_mock(prompt, model=task_type)

# 实例化供外部导入
gemini_client = GeminiClient()
