from bs4 import BeautifulSoup
import json
import re

# ====== 配置 ======
INPUT_HTML = "index.html"
OUTPUT_HTML = "index_with_i18n.html"
OUTPUT_JSON = "i18n.json"

# ====== 简单翻译占位函数 ======
def fake_translate(text, lang):
    translations = {
        "en": f"[EN]{text}",
        "zh-CN": text,  # 原始内容当简体
        "zh-TW": f"[繁]{text}",
        "ko": f"[한]{text}",
        "ja": f"[日]{text}"
    }
    return translations.get(lang, text)

# ====== Key 生成函数 ======
def slugify(text):
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^\w\-]", "", text)
    return text.lower()

# ====== 读取 HTML ======
with open(INPUT_HTML, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

translations = {}
counter = 1

# ====== 扫描标签 ======
for el in soup.find_all(["h1","h2","h3","h4","h5","h6","p","span","a","button","li"]):
    text = el.get_text(strip=True)
    if not text:
        continue  # 跳过空标签
    
    if "data-i18n" not in el.attrs:
        # 自动生成 key
        key = slugify(text) or f"auto_key_{counter}"
        el["data-i18n"] = key
        counter += 1
    else:
        key = el["data-i18n"]

    # 建立翻译字典
    if key not in translations:
        translations[key] = {
            "en": fake_translate(text, "en"),
            "zh-CN": fake_translate(text, "zh-CN"),
            "zh-TW": fake_translate(text, "zh-TW"),
            "ko": fake_translate(text, "ko"),
            "ja": fake_translate(text, "ja")
        }

# ====== 写回 HTML ======
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(str(soup))

# ====== 写翻译 JSON ======
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(translations, f, ensure_ascii=False, indent=4)

print(f"已生成 {OUTPUT_HTML} 和 {OUTPUT_JSON}")
