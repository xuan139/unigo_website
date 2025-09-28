import sqlite3
import os

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

# ⚡️ 新的 QA  数据
QA_DATA = [
    ("為什麼插上裝置後無反應？", "請確認 Type-C 接口支援資料傳輸，並重新插拔裝置"),
    ("HDMI 無訊號怎麼辦？", "確認設備支援 DP Alt Mode，並使用符合規格的 HDMI 線"),
    ("為什麼網路接口無法連線？", "請確認已正確插入網路線，並檢查設備是否開啟網路功能"),
    ("裝置溫度過高正常嗎？", "長時間使用或高效能運作下，輕微發熱屬於正常現象，請保持通風環境"),
    ("系統無法辨識擴充裝置？", "請重新啟動設備，或將裝置插入其他 USB-C 接口測試"),
    ("如何安全移除裝置？", "請先在作業系統中選擇「退出」或「安全移除硬體」，再拔除裝置")
]

def reset_qa_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 清空表数据
    cursor.execute("DELETE FROM qa_list")
    conn.commit()
    print("🗑️ QA 表数据已清空！")

    # 插入新的 QA 数据
    cursor.executemany('''
        INSERT INTO qa_list (question, answer)
        VALUES (?, ?)
    ''', QA_DATA)

    conn.commit()
    conn.close()
    print(f"✅ 已重新插入 {len(QA_DATA)} 条 QA 数据！")

if __name__ == '__main__':
    reset_qa_data()
