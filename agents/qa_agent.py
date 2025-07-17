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
    passages = vectordb.search_with_source(query, k=3)
    context = "\n".join([f"[{src}] {txt}" for txt, src in passages])

    template = input.get("template", "default")
    prompt_template = load_prompt_template(template)
    prompt = prompt_template.replace("{context}", context).replace("{query}", query)

    answer = gemini_client.smart_call(prompt, "qa")
    return {"qa_result": answer, "evidence": context, "template": template}

