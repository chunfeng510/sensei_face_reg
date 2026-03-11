"""測試應用程式是否能正常初始化"""
import sys
import traceback

print("=" * 60)
print("測試應用程式初始化...")
print("=" * 60)

try:
    print("\n1. 載入環境變數...")
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ 環境變數載入成功")
    
    print("\n2. 測試資料庫連線...")
    import os
    import pymysql
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    print(f"✓ 資料庫連線成功: {os.getenv('DB_NAME')}")
    conn.close()
    
    print("\n3. 導入 Flask 應用程式...")
    from app import app, db
    print("✓ Flask app 導入成功")
    
    print("\n4. 測試應用程式 context...")
    with app.app_context():
        print("✓ App context 建立成功")
        
        print("\n5. 測試資料庫查詢...")
        from models.person import Person
        persons = Person.query.all()
        print(f"✓ 查詢成功，目前有 {len(persons)} 個 person 記錄")
    
    print("\n" + "=" * 60)
    print("✓ 所有測試通過！應用程式應該能正常運作")
    print("=" * 60)
    
except Exception as e:
    print("\n" + "=" * 60)
    print("✗ 發生錯誤:")
    print("=" * 60)
    print(f"\n錯誤類型: {type(e).__name__}")
    print(f"錯誤訊息: {str(e)}")
    print("\n完整錯誤堆疊:")
    print("-" * 60)
    traceback.print_exc()
    print("-" * 60)
    sys.exit(1)
