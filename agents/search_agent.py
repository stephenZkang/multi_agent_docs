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
    qa_result = input.get("qa_result", "")
    evidence = input.get("evidence", "")
    query = input if isinstance(input, str) else input.get("input", "")
    
    web_evidence = web_search(query)
    logger.info(f"[search_agent] web evidence: {web_evidence}")
    
    return {
        "input": query,
        "search_result":  f"网络检索：{web_evidence}",
        "evidence": evidence,
        "qa_result": qa_result
    }
