from core.cache import cached_response

def run(input):
    content = input.get("qa_result", "")
    query = input.get("input", "")
    evidence = input.get("evidence", "")
    print(f"[TRANSLATE_AGENT DEBUG]...")
    prompt = f"请将以下文本翻译为英文：\n{content}"
    translated = cached_response(prompt, "translate")
    return {
        "input": query,
        "translated": translated,
        "qa_result": content,
        "evidence": evidence
    }
