from core.cache import cached_response

def run(input):
    search_result = input.get("search_result", "")
    qa_result = input.get("qa_result", "")
    evidence = input.get("evidence", "")
    query = input.get("input", "")
    translated = input.get("translated", "")
    prompt = f"请将以下文本汇总概括：网络检索:{search_result}\n本地检索{qa_result}"
    summary = cached_response(prompt,"summary")

    return {
        "summary": summary,
        "evidence":  evidence,
        "qa_result":  qa_result,
        "input":  query,
        "translated": translated
    }
