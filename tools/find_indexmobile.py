import os

# 要搜索的关键词
target = "indexmobile.html"

# 要搜索的目录（假设你的 Flask 项目里模板在 templates/，静态资源在 static/）
search_dirs = ["templates", "static"]

def search_file(filepath, target):
    results = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                if target in line:
                    results.append((lineno, line.strip()))
    except Exception as e:
        print(f"无法读取 {filepath}: {e}")
    return results

def main():
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        for root, _, files in os.walk(search_dir):
            for filename in files:
                if filename.endswith((".html", ".js", ".css")):
                    filepath = os.path.join(root, filename)
                    hits = search_file(filepath, target)
                    if hits:
                        print(f"\n🔎 在 {filepath} 发现 {target}:")
                        for lineno, content in hits:
                            print(f"  行 {lineno}: {content}")

if __name__ == "__main__":
    main()
