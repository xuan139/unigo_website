from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

# Blueprint 定义
# template_folder 指定为 "templates/forum"，会自动从 Flask app 的 templates 下拼接
forum_bp = Blueprint(
    "forum", __name__,
    url_prefix="/forum",
    template_folder="templates/forum"   # 所有模板放在 templates/forum/
)

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'crm.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 返回类似字典的行
    return conn

# 论坛首页 - 显示帖子
# @forum_bp.route("/")
# def forum_index():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM forum_posts ORDER BY created_at DESC")
#     posts = cursor.fetchall()
#     conn.close()
#     return render_template("forum_index.html", posts=posts)

# from flask import request

POSTS_PER_PAGE = 5  # 每页显示帖子数

@forum_bp.route("/")
def forum_index():
    page = request.args.get("page", 1, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取总帖子数
    cursor.execute("SELECT COUNT(*) FROM forum_posts")
    total_posts = cursor.fetchone()[0]
    total_pages = (total_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE

    # 分页获取帖子
    offset = (page - 1) * POSTS_PER_PAGE
    cursor.execute(
        "SELECT * FROM forum_posts ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (POSTS_PER_PAGE, offset)
    )
    posts = cursor.fetchall()
    conn.close()

    return render_template(
        "forum_index.html",
        posts=posts,
        page=page,
        total_pages=total_pages
    )

# 查看单个帖子及评论
@forum_bp.route("/post/<int:post_id>")
def forum_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forum_posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM forum_comments WHERE post_id = ? ORDER BY created_at ASC", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return render_template("forum_post.html", post=post, comments=comments)

# 发布新帖子
@forum_bp.route("/new", methods=["GET", "POST"])
def forum_new_post():
    if request.method == "POST":
        username = request.form.get("username", "匿名")
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content:
            return render_template("forum_new.html", message="标题和内容不能为空")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Use NULL for user_id if username is "匿名"
        user_id = None if username == "匿名" else 0  # Adjust 0 to a valid user_id if authenticated
        cursor.execute("INSERT INTO forum_posts (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
        conn.commit()
        conn.close()
        return redirect(url_for("forum.forum_index"))
    return render_template("forum_new.html")

# 评论帖子
@forum_bp.route("/post/<int:post_id>/comment", methods=["POST"])
def forum_comment(post_id):
    content = request.form.get("content")
    if not content:
        return redirect(url_for("forum.forum_post", post_id=post_id))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # Use NULL for user_id for anonymous comments
    cursor.execute("INSERT INTO forum_comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, None, content))
    conn.commit()
    conn.close()
    return redirect(url_for("forum.forum_post", post_id=post_id))