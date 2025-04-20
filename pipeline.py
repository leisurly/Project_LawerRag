from import_json_to_mysql import Import_Json_To_Judgments
from chunk_json import Chunk_Content
from upload_qdrant import Upload_Qdrant
from loguru import logger
import sys
from main import run_qa


""" if __name__ == "__main__":
    Import_Json_To_Judgments()   # 1. 匯入 JSON → MySQL
    Chunk_Content(batch_size=100)  # 2. 切割 → 存 chunk 到 MySQL
    Upload_Qdrant()             # 3. 向量化 chunk → 上傳到 Qdrant

    # 4. 啟動問答互動模式（僅在互動模式下執行）
    if sys.stdin.isatty():
        query = "死刑的標準是什麼？"
        answer = run_qa(query)
        print("💬 回答：", answer)
    else:
        logger.warning("非互動執行環境，跳過 RAG 問答模式") """

# logger.info("Pipeline success !")
if __name__ == "__main__":
    from main import run_qa
    query = "請使用繁體中文"
    answer = run_qa(query)
    if "尚未初始化" in answer:
        logger.warning("⚠️ QA 系統尚未初始化，請稍後重試")
    else:       
        print("💬 回答：", answer)
    
