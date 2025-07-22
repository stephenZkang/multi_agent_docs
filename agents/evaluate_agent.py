from core.gemini_client import gemini_client
from core.prompt_utils import load_prompt_template
import json
import os

def run(input):
    result = input.get("result", "")
    prompt = load_prompt_template("evaluate.txt", {"result": result})
    model_result = gemini_client.smart_call(prompt, "evaluate")
    try:
        eval_result = json.loads(model_result)
        if isinstance(eval_result, dict) and "pass" in eval_result:
            return eval_result
    except Exception:
        pass
    # fallback: 只要不包含'失败'或'错误'就合格
    if "失败" in result or "错误" in result:
        return {"pass": False, "reason": "结果包含失败或错误"}
    return {"pass": True, "reason": "评估通过"} 