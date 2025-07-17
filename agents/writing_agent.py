from core.cache import cached_response

def run(input):
    summary = input.get("summary", "")
    prompt = f"请根据以下总结内容撰写一段商业介绍：\n{summary}"
    return {"result": cached_response(prompt, "writing")}
