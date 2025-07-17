from core.cache import cached_response

def run(input):
    content = input.get("translated", "")
    prompt = f"请检查以下内容是否符合 ESG 可持续发展原则，并指出问题点：\n{content}"
    return {"verified": cached_response(prompt, "verify")}
