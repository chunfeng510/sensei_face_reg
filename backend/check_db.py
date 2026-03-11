import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    cursor = conn.cursor()
    
    db_name = os.getenv('DB_NAME', 'sensei_face_reg')
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    result = cursor.fetchone()
    
    if result:
        print(f"✓ 資料庫 '{db_name}' 已存在")
        
        # 檢查表是否存在
        cursor.execute(f"USE {db_name}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ 發現 {len(tables)} 個表:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("✗ 資料庫中沒有表，需要執行 schema.sql")
    else:
        print(f"✗ 資料庫 '{db_name}' 不存在，需要建立")
    
    conn.close()
    
except Exception as e:
    print(f"✗ 連線失敗: {e}")
