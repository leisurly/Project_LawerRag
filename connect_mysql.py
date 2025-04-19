import mysql.connector

def Connect_Mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='Your username',
            password='Your password',
            port=3306, # if port different nned chang thr port number 
            database="Database" #which database you need connect 
        )
        
        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    except ConnectionError as e :
        print("資料庫連線失敗")
        exit(0) #   正常結束 