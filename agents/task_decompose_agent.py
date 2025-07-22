from core.gemini_client import gemini_client
from core.prompt_utils import load_prompt_template
import json
import os

def run(input):
    question = input.get("input", "")
    prompt = load_prompt_template("task_decompose.txt", {"question": question})
    result = gemini_client.smart_call(prompt, "task_decompose")
    try:
        tasks = json.loads(result)
        if isinstance(tasks, list):
            return {"tasks": tasks}
    except Exception:
        pass
    # fallback: 返回原始字符串
    return {"tasks": [{"task": result, "type": "auto"}]} 