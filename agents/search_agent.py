from core.vectordb import vectordb
import logging
import requests
from agents import summary_agent

def web_search(query):
    # 使用duckduckgo简易API做示例，可替换为更强大的API
    try:
        resp = requests.get(f"https://duckduckgo.com/html/?q={query}", timeout=5)
        if resp.status_code == 200:
            # 简单提取部分文本
            text = resp.text
            # 这里只做演示，实际可用bs4等提取摘要
            snippet = text[:500]
            return snippet
        else:
            return "[Web search failed]"
    except Exception as e:
        return f"[Web search error: {e}]"

def run(input):
    logger = logging.getLogger("search_agent")
    logger.info(f"[search_agent] input: {input}")
    query = input if isinstance(input, str) else input.get("input", "")
    local_results = vectordb.search(query, k=3)
    local_evidence = "\n".join(local_results)
    logger.info(f"[search_agent] local evidence: {local_evidence}")
    web_evidence = web_search(query)
    logger.info(f"[search_agent] web evidence: {web_evidence}")
    # 汇总本地和网络检索内容
    summary_input = {
        "search_result": f"本地检索：{local_evidence}\n网络检索：{web_evidence}",
        "input": query
    }
    summary = summary_agent.run(summary_input)
    return {
        "input": query,
        "search_result": summary_input["search_result"],
        "evidence": summary_input["search_result"],
        "qa_result": summary.get("summary", "")
    }
