import os
import sqlite3
import json

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

# 输出目录
OUTPUT_DIR = os.path.join("static", "i18n")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_translations_to_json():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询所有翻译数据
    cursor.execute("SELECT lang_code, trans_key, trans_value FROM translations")
    rows = cursor.fetchall()

    # 按语言构建结构：{ lang_code: { key: value, ... }, ... }
    translations = {}
    for lang, key, value in rows:
        if lang not in translations:
            translations[lang] = {}
        translations[lang][key] = value

    # 写入 JSON 文件
    for lang_code, data in translations.items():
        filepath = os.path.join(OUTPUT_DIR, f"{lang_code}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出成功：{filepath}")

    conn.close()

if __name__ == "__main__":
    export_translations_to_json()
