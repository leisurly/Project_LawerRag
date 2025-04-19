from connect_mysql import Connect_Mysql
def Close_Mysql(conn, cursor):
    cursor.close()
    conn.close()