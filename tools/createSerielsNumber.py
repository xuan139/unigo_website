import sqlite3
import os

# 数据库路径（保持不变）
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def create_serial_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建 serial_numbers 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS serial_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 插入指定序列号（如果不存在）
    serial_to_insert = "0AC3B7D0-0812-39AB-904C-4EF64288FBE0"
    cursor.execute('''
        INSERT OR IGNORE INTO serial_numbers (serial) VALUES (?)
    ''', (serial_to_insert,))

    conn.commit()
    conn.close()
    print("✅ serial_numbers 表已创建并插入序列号")

if __name__ == "__main__":
    create_serial_table()
