import sqlite3
import os
import random
import string
from werkzeug.security import generate_password_hash

def random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def init_db():
    # Define database path
    db_dir = os.path.join(os.path.dirname(__file__), 'db')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'crm.db')

    # Delete existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database at {db_path}")

    # Connect to SQLite database (creates new db)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create user_info table with password
    cursor.execute('''
        CREATE TABLE user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL
        )
    ''')

    # Create history table
    cursor.execute('''
        CREATE TABLE history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        )
    ''')

    # Create app_versions table
    cursor.execute('''
        CREATE TABLE app_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            version TEXT NOT NULL,
            build_version TEXT NOT NULL,
            patch TEXT,
            release_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')

    # Insert 3 random users with hashed passwords
    users = []
    for i in range(1, 4):
        name = f"User{i}"
        email = f"user{i}@example.com"
        phone = f"555-010{i}"
        pwd_plain = random_password()
        pwd_hash = generate_password_hash(pwd_plain)
        users.append((name, email, phone, pwd_hash))
        print(f"Created user: {name}, email: {email}, password: {pwd_plain}")  # 明文密码打印方便测试

    cursor.executemany('''
        INSERT INTO user_info (name, email, phone, password)
        VALUES (?, ?, ?, ?)
    ''', users)

    # Insert sample data into history (关联 user_id 1)
    cursor.execute('''
        INSERT INTO history (user_id, action, details)
        VALUES (?, ?, ?)
    ''', (1, 'Upload File', 'Uploaded MyApp_v1.0.app to server'))

    # Insert sample data into app_versions
    cursor.execute('''
        INSERT INTO app_versions (app_name, version, build_version, patch, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', ('MyApp', '1.0.0', '100', 'update.delta', 'Initial release'))

    # Commit changes
    conn.commit()

    # Print contents of all tables
    print(f"\nDatabase initialized at {db_path}")
    print("\n=== Table Contents ===")

    # Print user_info
    print("\nuser_info:")
    cursor.execute('SELECT * FROM user_info')
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}, Password Hash: {row[4]}")

    # Print history
    print("\nhistory:")
    cursor.execute('SELECT * FROM history')
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, User ID: {row[1]}, Action: {row[2]}, Timestamp: {row[3]}, Details: {row[4]}")

    # Print app_versions
    print("\napp_versions:")
    cursor.execute('SELECT * FROM app_versions')
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, App Name: {row[1]}, Version: {row[2]}, Build Version: {row[3]}, Patch: {row[4]}, Release Date: {row[5]}, Notes: {row[6]}")

    # Close connection
    conn.close()

if __name__ == '__main__':
    init_db()
