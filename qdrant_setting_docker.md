# Qdrant setting in Docker

## 安裝 Qdrant

```bash
docker pull qdrant/qdrant
```

## 啟動 Qdrant 容器

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
  qdrant/qdrant
```

- REST API: http://localhost:6333
- Web UI: http://localhost:6333/dashboard
- gRPC API: http://localhost:6334

## 使用 Python SDK 初始化客戶端

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
```

## 建立 Collection

```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)
```

## 插入向量資料

```python
from qdrant_client.models import PointStruct

points = [
    PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
    PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": ["Berlin", "London"]}),
    PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": ["Berlin", "Moscow"]}),
]

client.upsert(
    collection_name="test_collection",
    points=points
)
```

## 查詢向量

```python
search_result = client.search(
    collection_name="test_collection",
    query_vector=[0.2, 0.1, 0.9, 0.7],
    limit=3
)
```
