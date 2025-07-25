import os
import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for
import jwt
from werkzeug.security import check_password_hash

app = Flask(__name__)
SECRET_KEY = 'your_secret_key_here_change_this'  # 生产环境请换强密钥

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def authenticate(email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_info WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return user
    return None

def create_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

# 首页
@app.route('/')
def index():
    return render_template('index.html', message="欢迎访问我的简单网站！")

# 登录页面和提交
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST表单提交
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return render_template('login.html', error='请填写邮箱和密码')
    
    user = authenticate(email, password)
    if user:
        token = create_jwt(user['id'])
        # 登录成功，直接显示 token，方便调试
        return f"""
        <h3>登录成功！</h3>
        <p>你的 JWT Token (有效期2小时):</p>
        <textarea rows="5" cols="80" readonly>{token}</textarea><br/><br/>
        <a href="/">返回首页</a>
        """
    else:
        return render_template('login.html', error='邮箱或密码错误')


@app.route('/upload', methods=['GET'])
def upload():
    token = request.args.get('token')
    if not token or not verify_jwt(token):
        return redirect(url_for('login'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
