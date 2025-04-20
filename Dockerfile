FROM python:3.10-slim

# 安裝系統與網路診斷工具（新增 curl、ping）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製所有檔案
COPY . .

# 再次確認 static 與 templates 被複製（如有 .dockerignore 排除就會失敗）
COPY static/ static/
COPY templates/ templates/

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 FastAPI 埠口
EXPOSE 8000

# 容器啟動時執行 uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
