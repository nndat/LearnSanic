import sqlite3
import os

basedir = os.path.abspath('./db')
DB_PATH = os.path.join(basedir, 'blog.db')
print(DB_PATH)


def initdb():
    # create table
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            create_at DATE,
            title TEXT,
            content TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            create_at DATE,
            content TEXT,
            post_id INT,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    """)
    con.commit()
    con.close()


def get_connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def get_all_posts(num=None):
    con, cur = get_connect()
    if num is None:
        posts = cur.execute("""SELECT * FROM posts
                                ORDER BY create_at DESC""").fetchall()
    else:
        posts = cur.execute("SELECT * FROM posts").fetchmany(num)
    con.close()
    return posts


def get_post(id):
    con, cur = get_connect()
    post = cur.execute(f"SELECT * FROM posts WHERE id == {int(id)}").fetchone()
    con.close()
    return post


def get_comment(post_id):
    con, cur = get_connect()
    comments = cur.execute(
        f"SELECT * from comments WHERE post_id == {post_id}").fetchall()
    con.close()
    return comments


def add_post(post):
    title = post['title']
    content = post['content']
    create_at = post['create_at']

    con, cur = get_connect()

    cur.execute("""
        INSERT INTO posts (create_at, title, content)
        VALUES (?, ?, ?)
    """, (create_at, title, content))
    con.commit()
    con.close()


def add_comment(comment):
    content = comment['content']
    create_at = comment['create_at']
    post_id = comment['post_id']
    con, cur = get_connect()

    cur.execute("""
        INSERT INTO comments (create_at, content, post_id)
        VALUES (?, ?, ?)
    """, (create_at, content, post_id))
    con.commit()
    con.close()


def delete_post(id_post):
    con, cur = get_connect()
    cur.execute(f"DELETE FROM posts WHERE id=={id_post}")
    con.commit()
    con.close()


def update_post(post):
    con, cur = get_connect()
    cur.execute("""
        UPDATE posts
        SET create_at=?, title=?, content=?
        WHERE id==?
    """, (post['create_at'], post['title'], post['content'], post['id']))
    con.commit()
    con.close()
