import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

# 泰文翻译数据 (不带 id，让 SQLite 自增)
THAI_TRANSLATIONS_DATA = [
    ('th','page_title','OStation - แพลตฟอร์ม SSD เกมแบบ Plug-and-Play'),
    ('th','nav_brand','OStation'),
    ('th','nav_home','หน้าหลัก'),
    ('th','nav_product','สินค้า'),
    ('th','nav_updates','อัปเดต'),
    ('th','nav_guide','คู่มือ'),
    ('th','nav_faq','คำถามที่พบบ่อย'),
    ('th','nav_download','ดาวน์โหลด'),
    ('th','nav_support','สนับสนุน'),
    ('th','hero_title','Plug and Play. โซลูชัน SSD เกมที่ดีที่สุด'),
    ('th','hero_sub','ติดตั้งล่วงหน้าด้วย Steam, Epic, VM Windows11, ไดรเวอร์ และสภาพแวดล้อมเกมเต็มรูปแบบ เปิดเครื่องแล้วเล่นได้ทันที'),
    ('th','get_started','เริ่มต้นใช้งาน'),
    ('th','features_title','คุณสมบัติเด่น 3 ข้อ'),
    ('th','feature1_title','Plug & Play'),
    ('th','feature1_desc','เชื่อมต่อ SSD เข้ากับ Mac ของคุณแล้วใช้งานได้ทันทีโดยไม่ต้องติดตั้ง'),
    ('th','feature2_title','พร้อมเล่นเกม'),
    ('th','feature2_desc','ติดตั้ง Steam, Epic, ไลบรารีรันไทม์ และเกม AAA ส่วนใหญ่ล่วงหน้าแล้ว'),
    ('th','feature3_title','รองรับ VM'),
    ('th','feature3_desc','มาพร้อม VMware virtual machines เพื่อให้คุณเปิด Windows 11 ได้ทันที หรือเลือกติดตั้ง Ubuntu หรืออื่น ๆ ได้เอง'),
    ('th','product_support_title','รองรับสำหรับ Mac'),
    ('th','product_support_desc','OStation ได้รับการปรับแต่งสำหรับ macOS มอบประสิทธิภาพราบรื่นทุกระบบ ให้คุณเล่นได้ทุกที่'),
    ('th','product_support_li1','รองรับ USB-C และ Thunderbolt'),
    ('th','product_support_li2','รองรับ macOS Catalina ถึง Sonoma'),
    ('th','product_support_li3','ทำงานกับ M1/M2/M3'),
    ('th','updates_title','อัปเดตซอฟต์แวร์'),
    ('th','update1_version','เวอร์ชัน 1.2.3'),
    ('th','update1_desc','• ปรับปรุงความเข้ากันได้กับ macOS Sonoma\n• แก้ไขบั๊กการแสดงผล VM\n• เพิ่มเครื่องมือเปิดอัตโนมัติ'),
    ('th','update2_version','เวอร์ชัน 1.2.2'),
    ('th','update2_desc','• เพิ่มตัวติดตั้ง DXVK\n• อัปเดตไลบรารีเกมที่ติดตั้งล่วงหน้า'),
    ('th','guide_title','คู่มือติดตั้ง'),
    ('th','guide_step1_title','ขั้นตอนที่ 1: เสียบ SSD'),
    ('th','guide_step1_desc','เชื่อมต่อ SSD เข้ากับ Mac ของคุณผ่าน USB-C หรือ Thunderbolt'),
    ('th','guide_step2_title','ขั้นตอนที่ 2: เปิด Toolkit'),
    ('th','guide_step2_desc','เปิดแอป OStation เพื่อเริ่มต้นการเล่นเกมหรือ VM'),
    ('th','guide_step3_title','ขั้นตอนที่ 3: เริ่มเล่นเกม'),
    ('th','guide_step3_desc','เพลิดเพลินกับ Steam, Epic หรือเกมที่ตั้งค่าล่วงหน้าได้ทันที ไม่ต้องติดตั้ง'),
    ('th','faq_title','คำถามที่พบบ่อย'),
    ('th','faq_q1','ทำไม Mac ของฉันไม่ตรวจพบ SSD?'),
    ('th','faq_a1','โปรดตรวจสอบว่าระบบอนุญาตไดรฟ์ภายนอกใน ความปลอดภัยและความเป็นส่วนตัว แล้วลองเปลี่ยนพอร์ต USB'),
    ('th','faq_q2','Steam ไม่เปิดหรืออัปเดตอย่างถูกต้อง?'),
    ('th','faq_a2','ตรวจสอบให้แน่ใจว่าเชื่อมต่ออินเทอร์เน็ตและให้สิทธิ์แล้ว ลองใช้ Steam Repair Tool ที่ศูนย์ดาวน์โหลด'),
    ('th','faq_q3','ฉันจะกู้คืนสภาพแวดล้อม SSD ดั้งเดิมได้อย่างไร?'),
    ('th','faq_a3','ไปที่ศูนย์ดาวน์โหลดและรับอิมเมจการกู้คืนอย่างเป็นทางการ คุณอาจต้องใช้หมายเลขประจำเครื่อง SSD ของคุณ'),
    ('th','download_title','ดาวน์โหลดหรือสั่งซื้อทันที'),
    ('th','download_desc','รับเครื่องมือเวอร์ชันล่าสุดหรือสั่งซื้อแพ็คเกจ SSD ที่ตั้งค่าล่วงหน้า'),
    ('th','download_button','เยี่ยมชมศูนย์ดาวน์โหลด'),
    ('th','support_title','การตรวจสอบผลิตภัณฑ์'),
    ('th','support_label','กรอกหมายเลขประจำเครื่องผลิตภัณฑ์ของคุณ'),
    ('th','support_button','ตรวจสอบ'),
    ('th','footer_text','© 2025 OStation | ติดต่อ: support@gamessd.com | สงวนลิขสิทธิ์ทั้งหมด')
]

def insert_thai_translations():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 批量插入
    cursor.executemany('''
        INSERT OR REPLACE INTO translations (lang_code, trans_key, trans_value)
        VALUES (?, ?, ?)
    ''', THAI_TRANSLATIONS_DATA)

    conn.commit()
    conn.close()
    print(f"✅ 已插入 {len(THAI_TRANSLATIONS_DATA)} 条泰文翻译！")

if __name__ == '__main__':
    insert_thai_translations()
