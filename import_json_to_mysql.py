import os
import json
from connect_mysql import Connect_Mysql
from close_mysql import Close_Mysql
from datetime import datetime
from loguru import logger


def Import_Json_To_Judgments():
    json_folder = os.path.join(os.getcwd(), "Data", "Case_1996")
    conn, cursor = Connect_Mysql()

    batch = []
    batch_size = 500
    inserted = 0
    failed = 0

    try:
        for filename in os.listdir(json_folder):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(json_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    jid = data.get("JID")
                    jtitle = data.get("JTITLE")
                    raw = data.get("JDATE")
                    jdate = datetime.strptime(raw.strip(), "%Y%m%d").date()
                    jyear = data.get("JYEAR")
                    jcase = data.get("JCASE")
                    jno = data.get("JNO")
                    jfull = data.get("JFULL", "").replace("\n", " ").replace("\r", " ")
                    file_path = filename

                    batch.append(
                        (jid, jyear, jcase, jno, jdate, jtitle, jfull, file_path)
                    )

                    if len(batch) >= batch_size:
                        cursor.executemany(
                            """
                            INSERT IGNORE INTO Judgments
                            (jid, jyear, jcase, jno, jdate, jtitle, jfull, file_path)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                            batch,
                        )
                        conn.commit()
                        inserted += len(batch)
                        logger.info(f" 已成功匯入 {inserted} 筆資料")
                        batch.clear()

                except Exception as e:
                    logger.warning(f"[錯誤] 匯入 {filename} 時出錯：{e}")
                    failed += 1

        if batch:
            cursor.executemany(
                """
                INSERT IGNORE INTO Judgments
                (jid, jyear, jcase, jno, jdate, jtitle, jfull, file_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE jtitle = VALUES(jtitle), jfull = VALUES(jfull)
            """,
                batch,
            )
            conn.commit()
            inserted += len(batch)
            logger.info(f"一批匯入 {len(batch)} 筆，總筆數為 {inserted}")

    finally:
        Close_Mysql(conn, cursor)
        logger.info(f"JSON 判決匯入完成：成功 {inserted} 筆，失敗 {failed} 筆")
