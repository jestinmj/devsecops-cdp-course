from blogapi import db


def is_user_exists(email):
    cur = db.connection.cursor()

    cur.execute("SELECT email FROM users WHERE email=%s", [email])
    res = cur.rowcount
    cur.close()

    if res == 0:
        return False

    return True


def is_post_exists(post_id):
    cur = db.connection.cursor()

    cur.execute("SELECT id FROM posts WHERE id=%s", [post_id])
    res = cur.rowcount
    cur.close()

    if res == 0:
        return False

    return True

