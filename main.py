from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from agents import pdf_agent, qa_agent, search_agent, summary_agent, writing_agent, translate_agent, verify_agent, weather_agent

builder = StateGraph(dict)
builder.add_node("pdf_agent", RunnableLambda(pdf_agent.run))
builder.add_node("qa_agent", RunnableLambda(qa_agent.run))
builder.add_node("search_agent", RunnableLambda(search_agent.run))
builder.add_node("summary_agent", RunnableLambda(summary_agent.run))
builder.add_node("writing_agent", RunnableLambda(writing_agent.run))
builder.add_node("translate_agent", RunnableLambda(translate_agent.run))
builder.add_node("verify_agent", RunnableLambda(verify_agent.run))
builder.add_node("weather_agent", RunnableLambda(weather_agent.run))

builder.set_entry_point("pdf_agent")
builder.add_edge("pdf_agent", "qa_agent")
builder.add_edge("qa_agent", "search_agent")
builder.add_edge("search_agent", "summary_agent")
builder.add_edge("summary_agent", "writing_agent")
builder.add_edge("writing_agent", "translate_agent")
builder.add_edge("translate_agent", "verify_agent")
builder.add_edge("verify_agent", "weather_agent")
builder.add_edge("weather_agent", END)

graph = builder.compile()

import os
from core.logger import logger

def get_env_or_default(key, default):
    return os.environ.get(key, default)

if __name__ == "__main__":
    # 读取配置
    pdf_model = get_env_or_default("PDF_MODEL", "pypdf2")
    pdf_segment = get_env_or_default("PDF_SEGMENT", "paragraph")
    pdf_length = get_env_or_default("PDF_SEGMENT_LENGTH", "200")
    llm_provider = get_env_or_default("LLM_PROVIDER", "mock")
    qa_template = get_env_or_default("QA_TEMPLATE", "default")

    logger.info(f"PDF解析模型: {pdf_model} | 分段策略: {pdf_segment} | 分段长度: {pdf_length}")
    logger.info(f"LLM模型: {llm_provider} | 问答提示词模板: {qa_template}")
    print("多智能体文档问答系统，输入 /q 退出。\n")
    print(f"[配置] PDF解析模型: {pdf_model} | 分段策略: {pdf_segment} | 分段长度: {pdf_length}")
    print(f"[配置] LLM模型: {llm_provider} | 问答提示词模板: {qa_template}\n")
    while True:
        question = input("请输入你的问题（或输入 /weather 城市名 查询天气）：")
        if question.strip() == "/q":
            print("已退出。")
            break
        if question.strip().startswith("/weather"):
            city = question.strip().replace("/weather", "").strip()
            result = weather_agent.run({"city": city})
            print("天气：", result.get("weather_result"))
            continue
        # 传递配置参数到各 agent
        result = graph.invoke({
            "input": question,
            "model": pdf_model,
            "segment": pdf_segment,
            "length": int(pdf_length),
            "template": qa_template,
            "llm_provider": llm_provider
        })
        print("答案：", result.get("qa_result"))
        print("依据：\n", result.get("evidence"))