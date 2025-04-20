from connect_mysql import Connect_Mysql
from close_mysql import Close_Mysql
from langchain.schema import Document


def Get_Mysql_Doc(batch_size=1000, offset=0):
    conn, cursor = Connect_Mysql()
    try:
        cursor.execute(
            f"""
            SELECT jid, jtitle, jfull FROM Judgments
            WHERE jfull IS NOT NULL
            LIMIT {batch_size} OFFSET {offset}
        """
        )
        rows = cursor.fetchall()
        docs = [
            Document(
                page_content=f"【案件編號】{row['jid']}\n【案件標題】{row['jtitle']}\n【判決全文】\n{row['jfull']}",
                metadata={"jid": row["jid"]},
            )
            for row in rows
        ]
        return docs
    finally:
        Close_Mysql(conn, cursor)
