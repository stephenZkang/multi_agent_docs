
# Multi-Agent Document Intelligence Platform

本项目是一个基于多智能体（Multi-Agent）架构的文档智能处理平台，支持 PDF 文档解析、问答、摘要、写作、翻译、ESG 合规性校验等多种任务，适用于企业级知识管理与自动化办公场景。

## ✨ 主要特性

- 🤖 **多智能体协作优势**：
  - 多智能体流水线：不是单一模型直接问答，而是多个专职 Agent 依次协作，每一步都可独立处理（如检索、问答、摘要、写作、翻译、合规校验等），流程更细致、可扩展。
  - 可追溯多步结果：每个 Agent 的输出都可保留，便于溯源和多角度分析，而普通问答系统通常只返回最终答案。
  - 支持多任务复合处理：不仅能问答，还能自动生成摘要、商业文案、翻译、合规性检测等，功能远超一般知识问答。
  - 易于扩展：你可以很方便地插拔、重组 Agent，定制自己的文档智能处理流程。
  - 结构化输出：最终结果是结构化的 dict，可用于前端展示、自动化流程等。
- 📄 **PDF 文档解析**：自动批量读取 `documents/` 目录下的 PDF 文件，提取文本并嵌入向量数据库。
- 🔍 **向量检索**：基于 FAISS 和 Sentence Transformers 实现高效语义检索，向量库文件保存在 `data/` 目录。
- 💬 **智能问答与摘要**：支持基于文档内容的智能问答和自动摘要。
- ✍️ **自动写作与翻译**：可根据摘要自动生成商业介绍，并支持中英文互译。
- ✅ **ESG 合规性校验**：自动检测文本是否符合 ESG 可持续发展原则。

## 🗂️ 目录结构

   ```
   main.py                  # 主流程入口
   requirements.txt         # 依赖包列表
   agents/                  # 各智能体模块
   api/                     # 独立API接口（如qa_api）
   core/                    # 向量库、缓存、模型API等核心工具
   data/                    # 向量库文件（vector.index, metadata.pkl）等持久化数据
   ui/                      # 可选：前端或接口层
   tests/                   # 各 agent 的单元测试
   documents/               # PDF 文档存放目录
   prompts/                 # 提示词相关内容
   ```

## 🚀 快速开始

1. **安装依赖（需 Python 3.8+）**：

   ```bash
   pip install -r requirements.txt
   ```

2. **准备文档**
   - 将待处理的 PDF 文件放入 `documents/` 目录。

3. **命令行模式运行主程序**

   ```bash
   python main.py
   ```

   - 首次运行会自动解析 PDF 并构建向量库。
   - 控制台支持多轮问答。

4. **Web UI 模式（推荐）**

   ```bash
   streamlit run ui/app.py
   ```

   - 浏览器会自动弹出问答界面，输入问题即可获得答案。

5. **后端 API 服务模式**

   ```bash
   uvicorn api.qa_api:app --reload --port 8000
   ```

   - 启动后访问 http://localhost:8000/docs 查看接口文档。
   - 主要接口：
     - `POST /qa` 传入 JSON：`{"input": "你的问题", "template": "default"}`，返回问答结果。
     - `GET /ping` 健康检查。

## 📦 依赖说明

- Python 3.8+
- faiss-cpu
- sentence-transformers
- pypdf
- pdfplumber
- pymupdf
- langgraph
- langchain-core

## 🧪 单元测试

所有 agent 和核心模块均配有基础单元测试：

- `tests/agents/` 目录：各 agent 的测试类
- `tests/core/` 目录：核心模块（如 cache、logger、vectordb、gemini_client）的测试类

运行所有 agent 测试：

```bash
python -m unittest discover -s tests/agents
```

运行所有核心模块测试：

```bash
python -m unittest discover -s tests/core
```

你也可以单独运行某个测试文件，例如：

```bash
python -m unittest tests/agents/test_weather_agent.py
python -m unittest tests/core/test_cache.py
```

## 🐳 Docker 部署

1. 构建镜像：

   ```bash
   docker build -t multi-agent-docs .
   ```

2. 运行容器（Web UI 默认 8501 端口）：

   ```bash
   docker run -it --rm -p 8501:8501 \
     -v $PWD/documents:/app/documents \
     --env-file .env \
     multi-agent-docs
   ```

   - 可通过挂载 documents 目录和 .env 文件实现数据与配置持久化。
   - 访问 [http://localhost:8501](http://localhost:8501) 即可使用 Web 问答界面。

3. 命令行模式：

   ```bash
   docker run -it --rm \
     -v $PWD/documents:/app/documents \
     --env-file .env \
     multi-agent-docs \
     python main.py
   ```

## 🤝 贡献与许可

- 欢迎提交 issue 和 PR。
- 本项目采用 MIT 许可证。

## 📋 TODO

- 支持真实大模型 API 接入
- 增加 Web UI
- 多语言支持
- 更丰富的 Agent 任务


