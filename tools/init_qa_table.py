import sqlite3
import os

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def create_qa_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ QA 表创建完成！")

if __name__ == '__main__':
    create_qa_table()
