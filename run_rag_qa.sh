#!/bin/bash

echo "啟動 docker 容器中..."
docker compose --project-name rag up -d

# 稍微等一下，讓容器完成啟動（特別是 MySQL & Qdrant）
sleep 3

# 找到 rag-app 容器 ID（自動匹配名包含 rag-app 的容器）
CONTAINER=$(docker ps --filter "name=rag-app" --format "{{.ID}}" | head -n 1)

if [ -z "$CONTAINER" ]; then
  echo "找不到正在運行的 rag-app 容器！"
  echo "請確認 docker-compose.yml 是否正確，或容器名稱是否變動"
  exit 1
fi

echo "找到 rag-app 容器：$CONTAINER"
echo "啟動問答模式（main.py）..."

# 進入容器並執行 main.py
docker exec -it "$CONTAINER" python main.py
