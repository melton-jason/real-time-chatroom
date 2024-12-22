import dearpygui.dearpygui as dpg

from .chat_room import chatroom, poll_messages, get_dpg_room_id


def get_chatrooms(client):
    message_type, response = client.send_and_receive({
        "_message_type": "ROOMS"
    })

    if message_type == "OK":
        users = []
        other = []
        for room in response["info"]:
            room_id, room_name, createdby = room
            if createdby == client.username:
                users.append((room_id, room_name))
            else:
                other.append((room_id, room_name))
        return users, other


def create_new_room(sender, app_data, user_data):
    room_name_input, refresh, client = user_data
    room_name: str = dpg.get_value(room_name_input)
    message_type, response = client.send_and_receive({
        "_message_type": "CREATE_ROOM",
        "name": room_name.strip()
    })
    if message_type == "OK":
        parent = dpg.get_item_parent(room_name_input)
        dpg.delete_item(parent)
        reset_list(refresh, None, client)


def new_room_window(sender, app_data, user_data):
    refresh_button, client = user_data
    with dpg.window(label="Create New Room"):
        dpg.add_text("Room Name: ")
        room_name_input = dpg.add_input_text()
        dpg.add_button(label="Create Room", user_data=(
            room_name_input, refresh_button, client), callback=create_new_room)


def join_room(sender, app_data, user_data):
    room_id, client = user_data
    room_name = dpg.get_item_label(sender)
    dpg_room_id = get_dpg_room_id(room_id, room_name)
    if dpg.does_item_exist(dpg_room_id):
        dpg.show_item(dpg.get_item_parent(dpg_room_id))
        poll_messages(client, room_id, room_name)
    else:
        chatroom(client, room_id, room_name)


def reset_list(sender, app_data, user_data):
    client = user_data
    parent_pos = dpg.get_item_pos("chatrooms")
    parent_width = dpg.get_item_width("chatrooms")
    parent_height = dpg.get_item_height("chatrooms")
    dpg.delete_item("chatrooms")
    chatroom_list(client, pos=parent_pos,
                  width=parent_width, height=parent_height)


def chatroom_list(client, pos=None, width=None, height=None):
    users_rooms, other_rooms = get_chatrooms(client)
    pos = (10, 200) if pos is None else pos
    height = 200 if height is None else height
    width = 200 if width is None else width
    with dpg.window(label="Chatrooms", tag="chatrooms", pos=pos, width=width, height=height):
        with dpg.group(horizontal=True):
            refresh_button = dpg.add_button(
                label="Refresh", user_data=client, callback=reset_list)
            dpg.add_button(label="Create New Room",
                           user_data=(refresh_button, client), callback=new_room_window)
        dpg.add_text("Your Chatrooms:")
        for room in users_rooms:
            room_id, room_name = room
            dpg.add_button(label=room_name, user_data=(
                room_id, client), callback=join_room)
        dpg.add_text("Other Chat Rooms: ")
        for room in other_rooms:
            room_id, room_name = room
            dpg.add_button(label=room_name, user_data=(
                room_id, client), callback=join_room)
