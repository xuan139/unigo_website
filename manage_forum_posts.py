import sqlite3

import os

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def show_posts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM forum_posts ORDER BY id;")
    posts = cursor.fetchall()

    if not posts:
        print("❌ 没有任何帖子。")
        return False

    print("\n=== 当前帖子列表 ===")
    for pid, title in posts:
        print(f"[{pid}] {title}")
    print("=====================\n")
    return True

def delete_posts(conn, ids):
    cursor = conn.cursor()
    deleted = 0
    for pid in ids:
        # 删除评论（外键手动处理）
        cursor.execute("DELETE FROM forum_comments WHERE post_id = ?;", (pid,))
        # 删除帖子
        cursor.execute("DELETE FROM forum_posts WHERE id = ?;", (pid,))
        deleted += cursor.rowcount
    conn.commit()
    print(f"✅ 已删除 {deleted} 条帖子及相关评论。")

def main():
    conn = sqlite3.connect(DB_PATH)

    if not show_posts(conn):
        return

    ids_input = input("请输入要删除的帖子ID（可多个，用逗号分隔）: ").strip()
    if not ids_input:
        print("未输入ID，已取消。")
        return

    try:
        ids = [int(i.strip()) for i in ids_input.split(",") if i.strip().isdigit()]
    except ValueError:
        print("❌ 输入格式错误，请输入数字ID。")
        return

    if not ids:
        print("❌ 没有有效的ID。")
        return

    confirm = input(f"确认删除ID {ids} 吗？(y/N): ").lower()
    if confirm != 'y':
        print("已取消操作。")
        return

    delete_posts(conn, ids)
    conn.close()

if __name__ == "__main__":
    main()
