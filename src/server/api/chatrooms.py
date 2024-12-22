import datetime

from typing import List, Tuple, Optional
from server.database import get_DB_connection


def get_chatroom_info():
    conn = get_DB_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT ch.id, ch.name, us.username FROM Chatroom ch LEFT JOIN User us ON us.id=ch.createdby")
    rows: List[Tuple[int, str, Optional[str]]] = cur.fetchall()
    conn.close()
    return rows


def create_chatroom(name, createdby: Optional[int] = None):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (name, createdby)
    try:
        cur.execute(
            "INSERT INTO Chatroom (name, createdby) VALUES (?, ?)", params)
        conn.commit()
    except:
        conn.close()
        return False
    finally:
        conn.close()
    return True


def get_messages(roomid):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (roomid,)
    cur.execute(
        "SELECT usr.username, mes.message FROM Message mes JOIN User usr ON usr.id=mes.userid WHERE chatroomid = ? ORDER BY timestamp", params)
    rows: List[Tuple[str, str]] = cur.fetchall()
    conn.close()
    return rows


def send_message(userid: int, chatroomid: int, message: str):
    conn = get_DB_connection()
    cur = conn.cursor()
    params = (userid, chatroomid, message, datetime.datetime.now())
    try:
        cur.execute(
            "INSERT INTO Message (userid, chatroomid, message, timestamp) VALUES (?, ?, ?, ?)", params)
        conn.commit()
    except:
        conn.close()
        return False
    finally:
        conn.close()
    return True
