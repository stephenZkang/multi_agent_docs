from core.gemini_client import gemini_client
from core.vectordb import vectordb

import os

def load_prompt_template(name):
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "prompts", f"qa_{name}.txt")
    if not os.path.exists(path):
        path = os.path.join(base, "prompts", "qa_default.txt")
    with open(path, encoding="utf-8") as f:
        return f.read()

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
        prompt_template = load_prompt_template(template)
    else:
        print("[QA_AGENT] 未检索到文档内容，使用兜底模板作答。")
        # 兜底模板命名为 qa_fallback.txt，不存在则用默认模板
        try:
            prompt_template = load_prompt_template("fallback")
        except Exception:
            prompt_template = load_prompt_template(template)

    prompt = prompt_template.replace("{context}", context).replace("{query}", query)

    answer = gemini_client.smart_call(prompt, "qa")
    return {"qa_result": answer, "evidence": context, "template": template}

