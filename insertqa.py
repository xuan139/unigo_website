import sqlite3
import os

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

# QA mock 数据
QA_DATA = [
    ("什么是 NVMe SSD？", "NVMe 是一种为固态硬盘设计的高速传输协议，相比 SATA SSD 拥有更高的读写速度，特别适合需要快速加载的游戏应用。"),
    ("如何将 Steam 游戏安装到外部 SSD？", "在 Steam 客户端设置中添加外部 SSD 为新的库文件夹，然后在安装游戏时选择该路径即可。"),
    ("Steam Deck 支持更换 SSD 吗？", "是的，Steam Deck 使用 M.2 2230 NVMe 接口的 SSD，可以更换，但需要注意尺寸兼容和数据备份。"),
    ("SSD 对游戏加载速度有多大提升？", "相比传统机械硬盘，SSD 能将游戏加载时间减少一半以上，尤其在大型开放世界游戏中效果显著。"),
    ("如何迁移 Steam 游戏到新的 SSD？", "复制 Steam 库文件夹到新 SSD 后，在 Steam 设置中添加该库路径，然后可以移动或重新识别游戏。"),
    ("我可以在多个硬盘之间共享 Steam 游戏吗？", "可以，Steam 支持多个库位置，只需在设置中添加多个安装目录即可按需选择。"),
    ("SSD 会影响游戏帧率吗？", "不会直接影响帧率，但可以显著提升加载速度和减少卡顿，尤其在读取大量资源时。"),
    ("如何检查我的 SSD 是否支持 PCIe 4.0？", "可通过主板说明书或系统信息工具（如 CrystalDiskInfo）查看接口类型和协议支持情况。"),
    ("Steam 游戏能否安装到移动硬盘？", "可以，但推荐使用 SSD 移动硬盘，否则加载速度和游戏体验可能受到影响。"),
    ("购买游戏前如何确认是否支持我的 SSD？", "一般无需特别担心兼容性，Steam 游戏对硬盘要求较低，只需确保有足够的存储空间即可。")
]

def reset_qa_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 清空表数据
    cursor.execute("DELETE FROM qa_list")
    conn.commit()
    print("🗑️ QA 表数据已清空！")

    # 重新插入 mock 数据
    cursor.executemany('''
        INSERT INTO qa_list (question, answer)
        VALUES (?, ?)
    ''', QA_DATA)

    conn.commit()
    conn.close()
    print(f"✅ 已重新插入 {len(QA_DATA)} 条 QA 数据！")

if __name__ == '__main__':
    reset_qa_data()
