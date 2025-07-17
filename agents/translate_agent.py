from core.cache import cached_response

def run(input):
    content = input.get("result", "")
    prompt = f"请将以下文本翻译为英文：\n{content}"
    return {"translated": cached_response(prompt, "translate")}
