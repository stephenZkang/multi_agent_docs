from core.gemini_client import gemini_client
from core.vectordb import vectordb
from core.prompt_utils import load_prompt_template


def run(input):
    query = input.get("input", "")
    print(f"[QA_AGENT DEBUG] input: {input}")
    passages = vectordb.search_with_source(query, k=3)
    context = "\n".join([f"[{src}] {txt}" for txt, src in passages])
    print(f"[QA_AGENT DEBUG] context: {context}")

    template = input.get("template", "default")
    # 区分兜底模板和基于内容的模板
    if context.strip():
        print(f"[QA_AGENT] 检索到文档内容，上下文如下:\n{context}")
        prompt_template = load_prompt_template(f"qa_{template}.txt", {"context": context, "query": query})
    else:
        print("[QA_AGENT] 未检索到文档内容，使用兜底模板作答。")
        try:
            prompt_template = load_prompt_template("qa_fallback.txt", {"context": context, "query": query})
        except Exception:
            prompt_template = load_prompt_template(f"qa_{template}.txt", {"context": context, "query": query})

    prompt = prompt_template
    answer = gemini_client.smart_call(prompt, "qa")
    return {"input": query, "qa_result": answer, "evidence": context, "template": template}

