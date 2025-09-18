import os
import pymysql
import datetime
from forum_app import forum_bp
import pandas as pd
from datetime import timedelta

from functools import wraps
from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, make_response, send_from_directory,session

)
import jwt
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
SECRET_KEY = 'StrongPassword123'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')

# 设置 session 永久化，并设置过期时间
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

# -------------------- MySQL 配置 --------------------
MYSQL_HOST = '18.183.186.19'
MYSQL_PORT = 3306
MYSQL_USER = 'unigo_remote'
MYSQL_PASSWORD = 'StrongPassword123!'
MYSQL_DB = 'crm'

# -------------------- 工具函数 --------------------

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def get_db_connection():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 返回字典
    )
    return conn

def authenticate(email, password):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM user_info WHERE email=%s', (email,))
        user = cursor.fetchone()
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
# 入口页面
@app.route('/crm')
@require_auth
def portal():
    return render_template('base.html')

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT question, answer FROM qa_list ORDER BY created_at DESC")
        qa_list = cursor.fetchall()
    conn.close()
    return render_template('index.html', qa_list=qa_list, message="欢迎访问！")

app.register_blueprint(forum_bp)

@app.route('/buy')
def buy():
    return render_template('buy.html')

# -------------------- 登录 --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    token = request.cookies.get('token')
    if token and verify_jwt(token):
        # session.permanent = True  # 激活永久 session，使用上面的 lifetime
        return redirect(url_for('upload'))

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
    response = redirect(url_for('login'))
    response.set_cookie('token', '', expires=0)
    return response

# -------------------- 上传 App 版本 --------------------
@app.route('/upload', methods=['GET', 'POST'])
@require_auth
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        version = request.form.get('version', '1.0.0')
        build_version = request.form.get('build_version', '1')
        patch = request.form.get('patch', '')
        notes = request.form.get('notes', '')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 计算文件大小
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_str = f"{file_size_mb:.2f} MB"

            full_notes = f"{notes.strip()}\n\n[File Size: {file_size_str}]"

            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app_versions (app_name, version, build_version, patch, notes)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (filename, version, build_version, patch, full_notes))
            conn.commit()
            conn.close()
            return redirect(url_for('downloads'))

    return render_template('upload.html')

@app.route('/downloads')
@require_auth
def downloads():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT app_name, version, build_version, patch, release_date, notes FROM app_versions ORDER BY release_date DESC")
        rows = cursor.fetchall()
    conn.close()

    files = [
        {
            'name': row['app_name'],
            'version': row['version'],
            'desc': row['build_version'],
            'platform': row['patch'],
            'date': row['release_date'],
            'notes': row['notes']
        } for row in rows
    ]
    return render_template('downloads.html', files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete')
@require_auth
def delete_page():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT app_name, version, build_version, patch, release_date FROM app_versions ORDER BY release_date DESC")
        rows = cursor.fetchall()
    conn.close()

    files = [
        {
            'name': row['app_name'],
            'version': row['version'],
            'desc': row['build_version'],
            'platform': row['patch'],
            'date': row['release_date']
        } for row in rows
    ]
    return render_template('delete.html', files=files)

@app.route('/delete-file', methods=['POST'])
@require_auth
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            return jsonify({'error': 'File not found on disk'}), 404

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM app_versions WHERE app_name=%s', (filename,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -------------------- QA 功能 --------------------
@app.route('/qa', methods=['GET'])
def qa_list():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, question, answer, created_at FROM qa_list ORDER BY created_at DESC")
        qa_list = cursor.fetchall()
    conn.close()
    return render_template('qa_list.html', qa_list=qa_list)

@app.route('/qa/edit', methods=['GET', 'POST'])
@require_auth
def qa_edit():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()
            if not question or not answer:
                cursor.execute("SELECT * FROM qa_list ORDER BY created_at DESC")
                qa_list = cursor.fetchall()
                return render_template('qa_edit.html', qa_list=qa_list, message="问题或答案不能为空")
            cursor.execute("INSERT INTO qa_list (question, answer) VALUES (%s, %s)", (question, answer))
            conn.commit()
        cursor.execute("SELECT * FROM qa_list ORDER BY created_at DESC")
        qa_list = cursor.fetchall()
    conn.close()
    return render_template('qa_edit.html', qa_list=qa_list, message="操作完成")

@app.route('/qa/editqa/<int:qa_id>', methods=['GET', 'POST'])
@require_auth
def edit_qa(qa_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, question, answer FROM qa_list WHERE id=%s", (qa_id,))
        qa = cursor.fetchone()
        if not qa:
            return redirect(url_for('qa_edit', message="记录不存在"))
        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()
            if not question or not answer:
                return render_template('qa_edit_form.html', qa=qa, message="问题或答案不能为空")
            cursor.execute("UPDATE qa_list SET question=%s, answer=%s WHERE id=%s", (question, answer, qa_id))
            conn.commit()
    conn.close()
    return redirect(url_for('qa_edit', message="编辑成功"))

@app.route('/qa/deleteqa/<int:qa_id>', methods=['GET', 'POST'])
@require_auth
def delete_qa(qa_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, question FROM qa_list WHERE id=%s", (qa_id,))
        qa = cursor.fetchone()
        if not qa:
            return redirect(url_for('qa_edit', message="记录不存在"))
        if request.method == 'POST':
            cursor.execute("DELETE FROM qa_list WHERE id=%s", (qa_id,))
            conn.commit()
    conn.close()
    return redirect(url_for('qa_edit', message="删除成功"))

# -------------------- Serial 功能 --------------------
def get_all_serials(search=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        if search:
            cursor.execute("SELECT serial FROM serial_numbers WHERE serial LIKE %s", (f"%{search}%",))
        else:
            cursor.execute("SELECT serial FROM serial_numbers")
        rows = cursor.fetchall()
    conn.close()
    return [r['serial'] for r in rows]

def get_serial(serial_number):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT serial FROM serial_numbers WHERE serial=%s", (serial_number,))
        row = cursor.fetchone()
    conn.close()
    return row['serial'] if row else None

def serial_exists(serial):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM serial_numbers WHERE serial=%s", (serial,))
        exists = cursor.fetchone() is not None
    conn.close()
    return "Exist" if exists else "Not exist"

@app.route("/serials_ajax", methods=["GET"])
@require_auth
def serials_ajax():
    search_query = request.args.get("search", "")
    result = serial_exists(search_query)
    return jsonify({"result": result})

@app.route("/serials", methods=["GET"])
@require_auth
def serials_page():
    search_query = request.args.get("search", "")
    serials = get_all_serials(search_query)
    return render_template("serials.html", serials=serials, search=search_query)

@app.route('/serial/<serial_number>', methods=['GET'])
@require_auth
def check_serial(serial_number):
    result = get_serial(serial_number)
    return jsonify({"serial": result}), 200

@app.route('/serial', methods=['POST'])
@require_auth
def add_serial():
    data = request.get_json()
    serial = data.get("serial")
    if not serial:
        return jsonify({"error": "serial is required"}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        try:
            cursor.execute("INSERT IGNORE INTO serial_numbers (serial) VALUES (%s)", (serial,))
            conn.commit()
        except:
            conn.close()
            return jsonify({"error": "serial already exists"}), 409
    conn.close()
    return jsonify({"serial": serial}), 201

@app.route('/uploadSS')
@require_auth
def upload_serial_page():
    # 这里渲染上传页面，模板中表单的 action 指向 /import_excel
    return render_template('uploadSS.html')


@app.route('/import_excel', methods=['POST'])
@require_auth
def import_excel_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        if file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        serials = df.iloc[:, 0].dropna().astype(str).tolist()
        conn = get_db_connection()
        added = 0
        with conn.cursor() as cursor:
            for s in serials:
                cursor.execute("INSERT IGNORE INTO serial_numbers (serial) VALUES (%s)", (s,))
                added += cursor.rowcount
        conn.commit()
        conn.close()
        return jsonify({"added": added, "total": len(serials)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/serials/delete_all', methods=['POST'])
@require_auth
def delete_all_serials():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM serial_numbers")
    conn.commit()
    conn.close()
    return redirect("/serials")

# ========================
# 主程序
# ========================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
