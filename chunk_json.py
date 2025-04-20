from get_mysql_doc import Get_Mysql_Doc
from connect_mysql import Connect_Mysql
from close_mysql import Close_Mysql
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger


def Chunk_Summary(doc):
    conn, cursor = Connect_Mysql()
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_text(doc.page_content)
        conn, cursor = Connect_Mysql()
        for i, chunk in enumerate(splits):
            chunk_inbox = chunk[:100]
            cursor.execute(
                """
            INSERT INTO JudgmentChunks (jid, chunk_index, chunk_text, chunk_inbox)
            VALUES (%s, %s, %s, %s)
        """,
                (doc.metadata["jid"], i, chunk, chunk_inbox),
            )
    except Exception as e:
        logger.warning("chunk summary error")
    conn.commit()
    Close_Mysql(conn, cursor)


def Chunk_Content(batch_size=100, batch_max=None):
    offset = 0
    batch_count = 0
    while True:
        docs = Get_Mysql_Doc(batch_size=batch_size, offset=offset)  # 整份文件
        if not docs:
            logger.info("沒有更多內文了！")
            break
        for doc in docs:
            Chunk_Summary(doc)
            logger.info("Chunk summary process..")

        offset += batch_size
        batch_count += 1
        if batch_max and batch_count >= batch_max:
            logger.info("finish chunk doc")
            break


if __name__ == "__main__":
    Chunk_Content(batch_size=100)


def Chunk_Summary(doc):
    conn, cursor = Connect_Mysql()
    try:
        jid = doc.metadata.get("jid", "UNKNOWN")
        if not doc.page_content:
            logger.warning(f"空內容略過: jid={jid}")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_text(doc.page_content)

        if not splits:
            logger.warning(f"沒有分到 chunk: jid={jid}")
            return

        for i, chunk in enumerate(splits):
            chunk_inbox = chunk[:20]
            logger.info(f"我現在得到第{i}的文字是{splits}")
            cursor.execute(
                """
                INSERT INTO JudgmentChunks (jid, chunk_index, chunk_text, chunk_inbox)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                chunk_text = VALUES(chunk_text),
                chunk_inbox = VALUES(chunk_inbox)
            """,
                (jid, i, chunk, chunk_inbox),
            )

        conn.commit()
        logger.info(f"jid={jid} 寫入 {len(splits)} 筆 chunk")
    except Exception as e:
        logger.warning(
            f"chunk summary error: jid={doc.metadata.get('jid', 'UNKNOWN')} | {e}"
        )
    finally:
        Close_Mysql(conn, cursor)


def Chunk_Content(batch_size=100, batch_max=None):
    offset = 0
    batch_count = 0
    while True:
        docs = Get_Mysql_Doc(batch_size=batch_size, offset=offset)  # 整份文件
        if not docs:
            logger.info("沒有更多內文了！")
            break
        for doc in docs:
            Chunk_Summary(doc)
            logger.info("Chunk summary process..")

        offset += batch_size
        batch_count += 1
        if batch_max and batch_count >= batch_max:
            logger.info("finish chunk doc")
            break


if __name__ == "__main__":
    Chunk_Content(batch_size=100)
