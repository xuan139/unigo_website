import sqlite3
import os

# 数据库路径（保持不变）
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def create_forum_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建 forum_posts 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        )
    ''')

    # 创建 forum_comments 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forum_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_id INTEGER,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES forum_posts(id),
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Forum tables created in crm.db (不会影响其他表)")

if __name__ == "__main__":
    create_forum_tables()
