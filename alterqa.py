import sqlite3
import os

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def add_image_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 增加 image_link 列，如果不存在的话
    cursor.execute('''
        ALTER TABLE qa_list
        ADD COLUMN image_link TEXT
    ''')

    conn.commit()
    conn.close()
    print("✅ 已为 qa_list 表增加 image_link 列！")

if __name__ == '__main__':
    add_image_column()
