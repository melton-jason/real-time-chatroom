import json

from typing import Tuple, Optional

from .api.users import create_user as db_create_user, get_user_id, get_user_info, user_login, log_user_off, InvalidPassword, UserDoesntExist

from .api.chatrooms import create_chatroom, get_chatroom_info, get_messages

from .api.chatrooms import send_message as db_send_messgae


def send_ok():
    return json.dumps({
        "_message_type": "OK"
    }).encode()


def send_fail(reason: Optional[str] = None):
    return json.dumps({
        "_message_type": "FAIL",
        "reason": reason
    }).encode()


def unhandled():
    pass


def login(args: dict):
    username = args["user_name"]
    password = args["password"]
    try:
        user_login(username, password)
    except InvalidPassword:
        return send_fail("Incorrect password")
    except UserDoesntExist:
        return send_fail(f"User {username} not found")
    except Exception as e:
        print(e)
        return send_fail(f"An error occured!: {e}")
    return send_ok()


def create_user(args: dict):
    username = args["user_name"]
    password = args["password"]
    if db_create_user(username, password):
        return send_ok()
    else:
        return send_fail()


def logout(args: dict):
    user = args["USER"]
    if log_user_off(user):
        return send_ok()
    return send_fail()


def get_users(args: dict):
    user_info = get_user_info()
    return json.dumps({
        "_message_type": "OK",
        "online": user_info["online"],
        "offline": user_info["offline"]
    }).encode()


def get_chatrooms(args: dict):
    chat_room_info = get_chatroom_info()
    return json.dumps({
        "_message_type": "OK",
        "info": chat_room_info
    }).encode()


def create_room(args: dict):
    user_id = get_user_id(args["USER"])
    name = args["name"]
    if create_chatroom(name, user_id):
        return send_ok()
    return send_fail()


def join_room(args: dict):
    room_id = args["roomid"]
    messages = get_messages(room_id)
    return json.dumps({
        "_message_type": "OK",
        "info": messages
    }).encode()


def send_message(args: dict):
    room_id = args["roomid"]
    message = args["message"]
    user_id = get_user_id(args["USER"])
    if db_send_messgae(user_id, room_id, message):
        return send_ok()
    return send_fail()


def parse_message(message: str) -> Tuple[str, dict]:
    data: dict = json.loads(message)
    if not isinstance(data, dict):
        return ""
    message_type = data.get('_message_type', None)
    args = {k: v for k, v in data.items() if not k == '_message_type'}
    return message_type, args


def handle_message(type: str):
    message = parse_message(type)
    message_type = message[0]
    args = message[1]
    match message_type:
        case "LOGIN": return login(args)
        case "CREATE_USER": return create_user(args)
        case "USERS": return get_users(args)
        case "ROOMS": return get_chatrooms(args)
        case "CREATE_ROOM": return create_room(args)
        case "ROOM_MESSAGES": return join_room(args)
        case "LOGOFF": return logout(args)
        case "MESSAGE": return send_message(args)
        case _: return unhandled()
