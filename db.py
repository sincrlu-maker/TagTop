"""
数据库连接与初始化（使用 Python 标准库 sqlite3，无需额外安装数据库驱动）
"""
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "tagtok.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nickname TEXT DEFAULT '',
    bio TEXT DEFAULT '',
    gender TEXT DEFAULT 'unknown',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT NOT NULL,
    author TEXT DEFAULT 'TagTok创作者'
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    video_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    watch_seconds REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(video_id) REFERENCES videos(id)
);

CREATE TABLE IF NOT EXISTS swipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    liked INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(from_user_id) REFERENCES users(id),
    FOREIGN KEY(to_user_id) REFERENCES users(id)
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(drop_existing=False):
    conn = get_connection()
    if drop_existing:
        conn.executescript(
            "DROP TABLE IF EXISTS interactions;"
            "DROP TABLE IF EXISTS swipes;"
            "DROP TABLE IF EXISTS videos;"
            "DROP TABLE IF EXISTS users;"
        )
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
