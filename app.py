import os
from flask import Flask, render_template, request
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html', message="欢迎访问我的简单网站！")

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/download')
def download():
    return render_template('download.html')

# 表单提交路由
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name', '匿名用户')
        return render_template('index.html', message=f"你好，{name}！感谢你的提交！")
    return render_template('index.html', message="请输入你的名字")

    # 上传文件路由
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            upload_dir = os.path.join('static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, file.filename))
            return render_template('upload.html', message=f"文件 {file.filename} 上传成功！")
        return render_template('upload.html', message="请上传有效文件！")
    return render_template('upload.html', message=None)

    # 下载页面路由
@app.route('/downloads')
def downloads():
    upload_dir = os.path.join('static', 'uploads')
    files = os.listdir(upload_dir) if os.path.exists(upload_dir) else []
    return render_template('downloads.html', files=files)

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
