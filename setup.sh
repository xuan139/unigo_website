
#!/bin/bash

# 设置项目名称和目录
PROJECT_NAME="unigo_website"
echo "创建项目目录: $PROJECT_NAME"

# 创建目录结构
mkdir -p $PROJECT_NAME/templates $PROJECT_NAME/static $PROJECT_NAME/build
cd $PROJECT_NAME

# 创建虚拟环境并激活
echo "创建 Python 虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装 Flask 和 Frozen-Flask
echo "安装 Flask 和 Frozen-Flask..."
pip install flask frozen-flask

# 创建 app.py
echo "创建 app.py..."
cat > app.py << 'EOF'
from flask import Flask, render_template, request
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html', message="欢迎访问我的简单网站！")

# 表单提交路由
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name', '匿名用户')
        return render_template('index.html', message=f"你好，{name}！感谢你的提交！")
    return render_template('index.html', message="请输入你的名字")

# 配置 Frozen-Flask 生成页面
@freezer.register_generator
def url_generator():
    yield 'index'
    yield 'submit'

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'freeze':
        freezer.freeze()  # 生成静态文件到 build/
    else:
        app.run(debug=True)
EOF

# 创建 index.html
echo "创建 templates/index.html..."
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>{{ message }}</h1>
    <form method="post" action="/submit">
        <label for="name">你的名字：</label>
        <input type="text" id="name" name="name">
        <button type="submit">提交</button>
    </form>
    <p><a href="/static/appcast.xml" download>下载 appcast.xml</a></p>
</body>
</html>
EOF

# 创建 style.css
echo "创建 static/style.css..."
cat > static/style.css << 'EOF'
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #333;
}
form {
    margin-top: 20px;
}
input, button {
    padding: 10px;
    margin: 5px;
}
p {
    line-height: 1.6;
}
EOF

# 创建 appcast.xml
echo "创建 static/appcast.xml..."
cat > static/appcast.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andreas-wilm.de/sparkle">
    <channel>
        <title>App Updates</title>
        <item>
            <title>OStation_V15.app Update</title>
            <sparkle:version>1.5</sparkle:version>
            <sparkle:shortVersionString>1.5</sparkle:shortVersionString>
            <sparkle:releaseNotesLink>https://unigo.com/updates/OStation_V15.app/release_notes_1.5.html</sparkle:releaseNotesLink>
            <pubDate>Tue, 22 Jul 2025 18:28:56 -0500</pubDate>
            <enclosure url="https://unigo.com/updates/OStation_V15.app/OStation_V15.app" sparkle:version="1.5" sparkle:shortVersionString="1.5" sparkle:fullSignature="full_sig" length="447640"/>
            <sparkle:deltaFromVersion>1.5</sparkle:deltaFromVersion>
            <sparkle:deltaUrl>https://unigo.com/updates/OStation_V15.app/upadte.delta</sparkle:deltaUrl>
            <sparkle:deltaSignature>delta_sig</sparkle:deltaSignature>
            <sparkle:deltaSize>6250</sparkle:deltaSize>
        </item>
    </channel>
</rss>
EOF

echo "项目创建完成！"
echo "进入项目目录: cd $PROJECT_NAME"
echo "激活虚拟环境: source venv/bin/activate"
echo "运行服务器: python3 app.py"
echo "生成静态文件: python3 app.py freeze"
echo "测试静态文件: cd build && python3 -m http.server 8000"
echo "测试下载: 访问 http://localhost:5000/static/appcast.xml 或 http://localhost:8000/static/appcast.xml"
