import streamlit as st
from main import graph

st.title("📄 多智能体 PDF 知识问答系统")

question = st.text_input("💬 输入你的问题（基于PDF文档）")

if st.button("提交") and question.strip():
    with st.spinner("分析文档并回答中..."):
        result = graph.invoke({"input": question})
        st.markdown("### ✅ 回答")
        st.write(result.get("qa_result", "无答案"))
        st.markdown("### 📚 引用段落")
        st.text(result.get("evidence", "无引用"))
