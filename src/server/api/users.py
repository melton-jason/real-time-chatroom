from server.database import get_DB_connection, hash_password


from typing import List, Tuple


class UserDoesntExist(Exception):
    ...


class InvalidPassword(Exception):
    ...


def authenticate_user(username: str, password: str):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (username,)
    res = cur.execute(
        "SELECT password, salt FROM User WHERE username = ?", params)
    rows: List[Tuple[str, str]] = res.fetchall()

    conn.close()
    if len(rows) != 1:
        raise UserDoesntExist

    db_password, salt = rows[0]
    if db_password == hash_password(password, salt)[0]:
        return True
    raise InvalidPassword


def user_login(username: str, password: str) -> bool:
    user_ok = authenticate_user(username, password)
    conn = get_DB_connection()
    cur = conn.cursor()
    if not user_ok:
        return False
    params = (username,)
    try:
        cur.execute("UPDATE User SET isonline=1 WHERE username = ?", params)
        conn.commit()
    except Exception as e:
        print(e, e.args)
        conn.close()
        return False
    cur.close()
    return True


def create_user(username: str, password: str):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (username,)
    res = cur.execute(
        "SELECT COUNT(*) FROM User WHERE username = ?", params)
    user_exists = res.fetchone()
    if user_exists is not None and user_exists[0] == 1:
        return user_login(username, password)
    hashed, salt = hash_password(password)
    params = (username, hashed, salt)
    try:
        cur.execute(
            "INSERT INTO User (username, password, salt, isonline) VALUES (?, ?, ?, 1)", params)
        conn.commit()
    except Exception as e:
        print(e, e.args)
        conn.close()
        return False
    conn.close()
    return True


def get_user_info():
    conn = get_DB_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, isonline FROM User")
    rows: List[Tuple[str, int]] = cur.fetchall()
    conn.close()
    online = []
    offline = []
    for row in rows:
        name, isonline = row
        if isonline == 1:
            online.append(name)
        else:
            offline.append(name)
    return {
        "online": online,
        "offline": offline
    }


def get_user_id(username: str):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (username,)
    cur.execute("SELECT id FROM User WHERE username = ?", params)
    row = cur.fetchone()
    conn.close()
    if row is not None:
        return int(row[0])
    return row


def log_user_off(username: str):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (username,)
    try:
        cur.execute(
            "UPDATE User SET isonline = 0 WHERE username = ?", params)
        conn.commit()
    except Exception as e:
        print(e, e.args)
        conn.close()
        return False
    conn.close()
    return True
