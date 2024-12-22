import dearpygui.dearpygui as dpg
import time
import threading

rooms = {}


def get_dpg_room_id(room_id, room_name):
    return f"room-({room_id}-{room_name})"


def close_room(sender, app_data, user_data):
    dpg_room_id = user_data
    global rooms
    rooms[dpg_room_id] = False
    dpg.hide_item(dpg.get_item_parent(dpg_room_id))


def send_message(sender, app_data, user_data):
    # Callback comes from the text field
    if len(user_data) == 2:
        room_id, client = user_data
        text_input = sender
    else:
        # Callback comes from the Send button
        room_id, text_input, client = user_data
    message: str = dpg.get_value(text_input)
    if message.strip() == "":
        return
    message_type, response = client.send_and_receive({
        "_message_type": "MESSAGE",
        "message": message,
        "roomid": room_id
    })
    dpg.set_value(text_input, '')


def chatroom(client, room_id, room_name):
    global rooms
    dpg_room_id = get_dpg_room_id(room_id, room_name)
    with dpg.window(label=room_name, user_data=dpg_room_id, on_close=close_room):
        with dpg.child_window(tag=dpg_room_id, resizable_y=False):
            pass
        with dpg.group(horizontal=True):
            input_text = dpg.add_input_text(user_data=(
                room_id, client), on_enter=True, callback=send_message)
            dpg.add_button(label="Send", user_data=(
                room_id, input_text, client), callback=send_message)
    poll_messages(client, room_id, room_name)


def get_chatroom_messages(client, room_id):
    message_type, response = client.send_and_receive({
        "_message_type": "ROOM_MESSAGES",
        "roomid": room_id
    })
    if message_type == "OK":
        return response["info"]


def poll_messages(client, room_id, room_name):
    dpg_room_id = get_dpg_room_id(room_id, room_name)
    global rooms
    if rooms.get(dpg_room_id, False):
        return
    rooms[dpg_room_id] = True
    message_poll = threading.Thread(
        target=update_chatroom, args=(client, room_id, room_name), daemon=True)
    message_poll.start()


def update_chatroom(client, room_id, room_name):
    global rooms
    dpg_room_id = get_dpg_room_id(room_id, room_name)
    while rooms.get(dpg_room_id, False):
        for item in dpg.get_item_children(dpg_room_id, 1):
            dpg.delete_item(item)
        messages = get_chatroom_messages(client, room_id)
        for message in messages:
            user_name, content = message
            dpg.add_text(f"{user_name}: {content}", parent=dpg_room_id)
        time.sleep(1)
