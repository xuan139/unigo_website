import os
import sqlite3
import datetime

from functools import wraps
from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, make_response, send_from_directory
)
import jwt
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
SECRET_KEY = 'your_secret_key_here'

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')  # or wherever your upload folder is

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')



# -------------------- 工具函数 --------------------
def get_db_connection():
    print("DB_PATH =", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def authenticate(email, password):
    print(email, password)

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_info WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return user
    return None



def create_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def require_auth(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        user_id = verify_jwt(token)
        if not user_id:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapper

# -------------------- 页面路由 --------------------

@app.route('/')
def index():
    return render_template('index.html', message="欢迎访问！")

@app.route('/buy')
def buy():
    return render_template('buy.html')


# -------------------- 登录 --------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    token = request.cookies.get('token')
    if token and verify_jwt(token):
        return redirect(url_for('upload'))  # ⬅️ 跳过重复登录

    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', message="请输入邮箱和密码")

    user = authenticate(email, password)
    if user:
        token = create_jwt(user['id'])
        resp = make_response(redirect(url_for('upload')))
        resp.set_cookie('token', token, httponly=True)
        return resp
    else:
        return render_template('login.html', message="邮箱或密码错误")

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))  # 退出后重定向到登录页（或 index）
    response.set_cookie('token', '', expires=0)  # 清除 JWT Cookie
    return response


# -------------------- 受保护页面 --------------------

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        version = request.form.get('version', '1.0.0')
        description = request.form.get('description', 'Initial Release')
        platform = request.form.get('platform', 'macOS / Windows')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # conn = sqlite3.connect(DB_PATH)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO app_versions (filename, version, description, platform)
                VALUES (?, ?, ?, ?)
            ''', (filename, version, description, platform))
            conn.commit()
            conn.close()

            return redirect(url_for('downloads'))

    return render_template('upload.html')



@app.route('/downloads')
def downloads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, version, description, platform, upload_date FROM app_versions ORDER BY upload_date DESC")
    rows = cursor.fetchall()
    conn.close()

    files = [
        {
            'name': row[0],
            'version': row[1],
            'desc': row[2],
            'platform': row[3],
            'date': row[4]
        } for row in rows
    ]
    return render_template('downloads.html', files=files)


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete-file', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    file_path = os.path.join('static', 'uploads', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/user_management', methods=['GET'])
@require_auth
def user_management():
    conn = get_db_connection()
    users = conn.execute('SELECT id, name, email, phone FROM user_info').fetchall()
    conn.close()
    return render_template('user_management.html', users=users)

# -------------------- 启动 --------------------

if __name__ == '__main__':
    # reset_app_versions_table()
    app.run(debug=True)
