import sqlite3


def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


def del_table():
    with sqlite3.connect("news.db") as db:
        cursor = db.cursor()
        cursor.execute(""" DROP TABLE IF EXISTS news """)


def create_table():
    with sqlite3.connect("news.db") as db:
        cursor = db.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS news(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                title TEXT NOT NULL,
                date_time DATE NOT NULL,
                link TEXT NOT NULL
            )""")


def add_news(new_title, new_date_time, new_link):
    with sqlite3.connect("news.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT link FROM news where link=?", (new_link,))
        data = cursor.fetchall()
        if not data:
            cursor.execute("INSERT INTO news (title, date_time, link) VALUES (?,?,?)",
                           (new_title, new_date_time, new_link))
            db.commit()
        last_new_id = cursor.lastrowid
    return None if last_new_id == 0 else last_new_id


def get_five_news():
    with sqlite3.connect("news.db") as db:
        db.row_factory = dict_factory
        cursor = db.cursor()
        cursor.execute("SELECT * FROM news ORDER BY date_time DESC LIMIT 5")
        res = cursor.fetchall()
    return res


def get_fifty_news():
    with sqlite3.connect("news.db") as db:
        db.row_factory = dict_factory
        cursor = db.cursor()
        cursor.execute("SELECT * FROM news ORDER BY date_time DESC LIMIT 50")
        res = cursor.fetchall()
    return res


def get_news_by_id(news_id):
    with sqlite3.connect("news.db") as db:
        db.row_factory = dict_factory
        cursor = db.cursor()
        cursor.execute("SELECT * FROM news WHERE id=?", (news_id,))
        res = cursor.fetchall()
    return res


if __name__ == '__main__':
    create_table()
