#!/usr/bin/env python3
import os
import sys
from PIL import Image

# ---------- 配置 ----------
# 替换成你的 PNG 文件名（放在 Documents 目录下）
SOURCE_PNG_NAME = "MyApp.png"
APP_NAME = "AppIcon"


# 用户 Documents 目录
home_dir = os.path.expanduser("~")
documents_dir = os.path.join(home_dir, "Documents")

source_png = os.path.join(documents_dir, SOURCE_PNG_NAME)
iconset_dir = os.path.join(documents_dir, f"{APP_NAME}.iconset")
icns_file = os.path.join(documents_dir, f"{APP_NAME}.icns")

# ---------- 图标尺寸列表 ----------
# macOS 常用尺寸
sizes = [
    16, 32, 64, 128, 256, 512, 1024
]

# ---------- 检查源 PNG ----------
if not os.path.exists(source_png):
    print(f"❌ 源 PNG 不存在: {source_png}")
    sys.exit(1)

# ---------- 创建 iconset 目录 ----------
if not os.path.exists(iconset_dir):
    os.makedirs(iconset_dir)

# ---------- 生成不同尺寸的 PNG ----------
im = Image.open(source_png)

for size in sizes:
    im_resized = im.resize((size, size), Image.LANCZOS)
    filename = os.path.join(iconset_dir, f"icon_{size}x{size}.png")
    im_resized.save(filename)
    print(f"✅ 生成 {filename}")

# macOS 还需要 2x 尺寸（Retina）
for size in sizes:
    im_resized = im.resize((size*2, size*2), Image.LANCZOS)
    filename = os.path.join(iconset_dir, f"icon_{size}x{size}@2x.png")
    im_resized.save(filename)
    print(f"✅ 生成 {filename}")

# ---------- 使用 iconutil 打包成 ICNS ----------
cmd = f"iconutil -c icns '{iconset_dir}' -o '{icns_file}'"
print(f"📦 生成 ICNS 文件: {icns_file}")
ret = os.system(cmd)
if ret == 0:
    print(f"✅ 成功生成 ICNS 文件: {icns_file}")
else:
    print("❌ 生成 ICNS 失败，请检查 iconutil 或 iconset 目录是否正确")
