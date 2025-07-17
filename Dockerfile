# 基于官方 Python 镜像的多智能体文档平台 Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目全部代码
COPY . .

# 默认暴露 Streamlit 端口
EXPOSE 8501

# 启动命令，可通过覆盖 CMD 切换为 main.py
CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
