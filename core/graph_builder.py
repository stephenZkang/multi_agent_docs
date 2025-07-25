from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableLambda
from agents import pdf_agent, qa_agent, search_agent, summary_agent, writing_agent, translate_agent, verify_agent, weather_agent

class GraphBuilder:
    def __init__(self):
        self.checkpointer = InMemorySaver()
        self.graph = self._build_graph()

    def _need_translate(self, state):
        query = state.get("input", "")
        print(f"[_need_translate query:{query}]")
        keywords = ["翻译", "translate", "英文", "英文版", "translate into english", "to english"]
        flag = any(k in query.lower() for k in keywords)
        if flag:
            print(f"[translate_agent is true]...")
            return "translate_agent"
        else:
            print(f"[search_agent is true]...")
            return "search_agent"

    def _build_graph(self):
        builder = StateGraph(dict)
        builder.add_node("pdf_agent", RunnableLambda(pdf_agent.run))
        builder.add_node("qa_agent", RunnableLambda(qa_agent.run))
        builder.add_node("translate_agent", RunnableLambda(translate_agent.run))
        builder.add_node("search_agent", RunnableLambda(search_agent.run))
        builder.add_node("summary_agent", RunnableLambda(summary_agent.run))
        # builder.add_node("writing_agent", RunnableLambda(writing_agent.run))
        builder.add_node("verify_agent", RunnableLambda(verify_agent.run))
        # builder.add_node("weather_agent", RunnableLambda(weather_agent.run))

        builder.set_entry_point("pdf_agent")
        builder.add_edge("pdf_agent", "qa_agent")
        # builder.add_edge("summary_agent", "writing_agent")
        # builder.add_edge("writing_agent", "translate_agent")
        # builder.add_edge("translate_agent", "verify_agent")
        # builder.add_edge("verify_agent", "weather_agent")
        # qa_agent -> translate_agent（有翻译意图）
        builder.add_conditional_edges("qa_agent", self._need_translate)
        # qa_agent -> verify_agent（无翻译意图）
        # builder.add_conditional_edges("qa_agent", "verify_agent", condition=lambda state: not self._need_translate(state))
        # translate_agent -> verify_agent
        builder.add_edge("translate_agent", "search_agent")
        builder.add_edge("search_agent", "summary_agent")
        builder.add_edge("summary_agent", "verify_agent")
        builder.add_edge("verify_agent", END)

        # 集成内存记忆
        return builder.compile(checkpointer=self.checkpointer)

    def get_graph(self):
        return self.graph

# 单例实例，兼容原有用法
graph = GraphBuilder().get_graph()
