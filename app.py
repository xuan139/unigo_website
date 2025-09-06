import os
import sqlite3
import datetime
from forum_app import forum_bp
import pandas as pd

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM qa_list ORDER BY created_at DESC")
    qa_list = cursor.fetchall()
    conn.close()

    # return render_template('index.html', qa_list=qa_list)
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
# @require_auth
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

            # ✅ 计算文件大小（字节 -> MB）
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_str = f"{file_size_mb:.2f} MB"

            # ✅ 拼接 notes
            full_notes = f"{notes.strip()}\n\n[File Size: {file_size_str}]"

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO app_versions (
                    app_name, version, build_version, patch, notes
                ) VALUES (?, ?, ?, ?, ?)
            ''', (filename, version, build_version, patch, full_notes))
            conn.commit()
            conn.close()

            return redirect(url_for('downloads'))

    return render_template('upload.html')



@app.route('/downloads')
# @require_auth
def downloads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT app_name, version,  build_version, patch, release_date ,notes FROM app_versions ORDER BY release_date DESC")
    rows = cursor.fetchall()
    conn.close()

    files = [
        {
            'name': row[0],
            'version': row[1],
            'desc': row[2],
            'platform': row[3],
            'date': row[4],
            'notes': row[5]
        } for row in rows
    ]
    return render_template('downloads.html', files=files)


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete')
# @require_auth
def delete_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT app_name, version, build_version, patch, release_date FROM app_versions ORDER BY release_date DESC")
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
        # 删除文件（如果存在）
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            return jsonify({'error': 'File not found on disk'}), 404

        # 删除数据库记录
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM app_versions WHERE app_name = ?', (filename,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/qa', methods=['GET'])
def qa_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question, answer, created_at FROM qa_list ORDER BY created_at DESC")
        qa_list = cursor.fetchall()
        conn.close()
        return render_template('qa_list.html', qa_list=qa_list)
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/qa/edit', methods=['GET', 'POST'])
def qa_edit():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()
            if not question or not answer:
                qa_list = cursor.execute("SELECT * FROM qa_list ORDER BY created_at DESC").fetchall()
                conn.close()
                return render_template('qa_edit.html', qa_list=qa_list, message="问题或答案不能为空")
            cursor.execute("INSERT INTO qa_list (question, answer) VALUES (?, ?)", (question, answer))
            conn.commit()
            qa_list = cursor.execute("SELECT * FROM qa_list ORDER BY created_at DESC").fetchall()
            conn.close()
            return render_template('qa_edit.html', qa_list=qa_list, message="添加成功")
        qa_list = cursor.execute("SELECT * FROM qa_list ORDER BY created_at DESC").fetchall()
        conn.close()
        return render_template('qa_edit.html', qa_list=qa_list, message=request.args.get('message'))
    except Exception as e:
        conn.close()
        return render_template('qa_edit.html', qa_list=[], message=f"错误: {str(e)}"), 500

@app.route('/qa/editqa/<int:qa_id>', methods=['GET', 'POST'])
def edit_qa(qa_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question, answer FROM qa_list WHERE id = ?", (qa_id,))
        qa = cursor.fetchone()
        if not qa:
            conn.close()
            return redirect(url_for('qa_edit', message="记录不存在"))
        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()
            if not question or not answer:
                conn.close()
                return render_template('qa_edit_form.html', qa=qa, message="问题或答案不能为空")
            cursor.execute("UPDATE qa_list SET question = ?, answer = ? WHERE id = ?", (question, answer, qa_id))
            conn.commit()
            conn.close()
            return redirect(url_for('qa_edit', message="编辑成功"))
        conn.close()
        return render_template('qa_edit_form.html', qa=qa)
    except Exception as e:
        conn.close()
        return redirect(url_for('qa_edit', message=f"编辑失败: {str(e)}"))

@app.route('/qa/deleteqa/<int:qa_id>', methods=['GET', 'POST'])
def delete_qa(qa_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question FROM qa_list WHERE id = ?", (qa_id,))
        qa = cursor.fetchone()
        if not qa:
            conn.close()
            return redirect(url_for('qa_edit', message="记录不存在"))
        if request.method == 'GET':
            conn.close()
            return render_template('qa_delete.html', qa_id=qa_id, question=qa['question'])
        cursor.execute("DELETE FROM qa_list WHERE id = ?", (qa_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('qa_edit', message="删除成功"))
    except Exception as e:
        conn.close()
        return redirect(url_for('qa_edit', message=f"删除失败: {str(e)}"))
# ========================
# 获取所有序列号，支持搜索
# ========================
def get_all_serials(search=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT serial FROM serial_numbers WHERE serial LIKE ?", (f"%{search}%",))
    else:
        cursor.execute("SELECT serial FROM serial_numbers")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

# ========================
# 单条序列号查询
# ========================
def get_serial(serial_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT serial FROM serial_numbers WHERE serial = ?", (serial_number,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# ========================
# 显示所有序列号页面 + 搜索
# ========================
def serial_exists(serial):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM serial_numbers WHERE serial = ?", (serial,))
    exists = cursor.fetchone() is not None
    conn.close()
    return "Exist" if exists else "Not exist"

@app.route("/serials_ajax", methods=["GET"])
def serials_ajax():
    search_query = request.args.get("search", "")
    result = serial_exists(search_query)
    return jsonify({"result": result})

@app.route("/serials", methods=["GET"])
def serials_page():
    search_query = request.args.get("search", "")
    serials = get_all_serials(search_query)
    return render_template("serials.html", serials=serials, search=search_query)

# ========================
# 查询单条序列号接口
# ========================
@app.route('/serial/<serial_number>', methods=['GET'])
def check_serial(serial_number):
    result = get_serial(serial_number)
    if result:
        return jsonify({"serial": result}), 200
    else:
        return jsonify({"serial": None}), 200

# ========================
# 添加单个序列号接口
# ========================
@app.route('/serial', methods=['POST'])
def add_serial():
    data = request.get_json()
    serial = data.get("serial")
    if not serial:
        return jsonify({"error": "serial is required"}), 400
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO serial_numbers (serial) VALUES (?)", (serial,))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "serial already exists"}), 409
    conn.close()
    return jsonify({"serial": serial}), 201

# ========================
# 批量导入 Excel / CSV 接口
# ========================
@app.route('/import_excel', methods=['POST'])
def import_excel():
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
        if df.empty:
            return jsonify({"error": "File is empty"}), 400

        serials = df.iloc[:, 0].dropna().astype(str).tolist()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        added = 0
        for s in serials:
            cursor.execute("INSERT OR IGNORE INTO serial_numbers (serial) VALUES (?)", (s,))
            added += cursor.rowcount
        conn.commit()
        conn.close()
        return jsonify({"added": added, "total": len(serials)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================
# 网页上传页面
# ========================
@app.route('/uploadSS', methods=['GET', 'POST'])
def upload_page():
    result_text = None
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            result_text = "choose file pls"
        else:
            try:
                if file.filename.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file)
                elif file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    result_text = "file is not support!"
                    return render_template('uploadSS.html', result=result_text)
                
                serials = df.iloc[:, 0].dropna().astype(str).tolist()
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                added = 0
                for s in serials:
                    cursor.execute("INSERT OR IGNORE INTO serial_numbers (serial) VALUES (?)", (s,))
                    added += cursor.rowcount
                conn.commit()
                conn.close()
                result_text = f"import successful，total amount: {len(serials)}, add successfully: {added}"
            except Exception as e:
                result_text = f"fail import: {e}"
    return render_template('uploadSS.html', result=result_text)

@app.route('/serials/delete_all', methods=['POST'])
def delete_all_serials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM serial_numbers")
    conn.commit()
    conn.close()
    return redirect("/serials")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)