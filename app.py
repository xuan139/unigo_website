import os
import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template
import jwt
from werkzeug.security import check_password_hash

app = Flask(__name__)
SECRET_KEY = 'your_secret_key_here_change_this'  # JWT密钥，生产环境请改成安全值

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

# 登录接口（示范用JSON接口）
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = authenticate(email, password)
    if user:
        token = create_jwt(user['id'])
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# 受保护上传示例接口
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # 验证 Authorization 头
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header missing or invalid'}), 401
    token = auth_header.split(' ')[1]
    user_id = verify_jwt(token)
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            upload_dir = os.path.join('static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, file.filename))

            # 记录上传历史
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO history (user_id, action, details) VALUES (?, ?, ?)",
                (user_id, 'Upload File', f'Uploaded {file.filename}')
            )
            conn.commit()
            conn.close()

            return jsonify({'message': f'File {file.filename} uploaded successfully'})
        return jsonify({'error': 'No valid file provided'}), 400

    # GET 请求返回上传页面（示范简单页面）
    return render_template('upload.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
