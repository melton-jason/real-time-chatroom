import dearpygui.dearpygui as dpg

from typing import Optional

from .protocol import Client
from .users import user_list
from .chat_rooms import chatroom_list
from .colors import COLORS

from settings import read_settings

client: Optional[Client] = None


def get_client():
    global client
    return client


def set_client(new_client: Optional[Client]):
    global client
    client = new_client
    return new_client


def handle_close():
    client = get_client()
    if client is not None and client.username is not None:
        client.send_and_receive({
            "_message_type": "LOGOFF"
        })


def connect_to_server(sender, app_data, user_data):
    host_input, port_input, error_message = user_data
    host_name, port = [dpg.get_value(host_input), dpg.get_value(port_input)]
    client = set_client(Client(host_name, port))
    if client.connect():
        dpg.set_viewport_title(f"Connected to: {host_name}")
        dpg.delete_item(dpg.get_item_parent(sender))
        login_window(client)
    else:
        dpg.show_item(error_message)
        dpg.set_value(error_message, f"Unable to connect to {
                      host_name}:{port}")


def login(sender, app_data, user_data):
    username_input, password_input, error_reason, client = user_data
    username, password = (dpg.get_value(
        username_input), dpg.get_value(password_input))
    message_type, response = client.send_and_receive({
        "_message_type": "LOGIN",
        "user_name": username,
        "password": password
    })
    if message_type == "OK":
        client.username = username
        dpg.delete_item(dpg.get_item_parent(sender))
        dpg.set_viewport_title(f"{username}: Connected to {client.hostname}")
        user_list(client)
        chatroom_list(client)
    elif message_type == "FAIL":
        reason = response["reason"]
        dpg.show_item(error_reason)
        dpg.set_value(error_reason, reason)


def create_user(sender, app_data, user_data):
    username_input, password_input, error_reason, client = user_data
    username, password = (dpg.get_value(
        username_input), dpg.get_value(password_input))
    message_type, response = client.send_and_receive({
        "_message_type": "CREATE_USER",
        "user_name": username,
        "password": password
    })
    if message_type == "OK":
        client.username = username
        dpg.delete_item(dpg.get_item_parent(sender))
        dpg.set_viewport_title(f"{username}: Connected to {client.hostname}")
        user_list(client)
        chatroom_list(client)
    elif message_type == "FAIL":
        reason = response["reason"]
        dpg.show_item(error_reason)
        dpg.set_value(error_reason, reason)


def connection_window():
    PORT = read_settings()['SERVER_PORT']
    height = dpg.get_viewport_client_height()
    width = dpg.get_viewport_client_width()
    with dpg.window(label="Connect to a Chat Server!", pos=(width//3, height//3), width=width//4):
        dpg.add_text('Host: ')
        host_name = dpg.add_input_text()
        dpg.add_text("Port: ")
        port = dpg.add_input_int(default_value=PORT)
        error_message = dpg.add_text(show=False, color=COLORS.RED)
        dpg.add_button(label="Connect!", user_data=(
            host_name, port, error_message), callback=connect_to_server)


def login_window(client):
    height = dpg.get_viewport_client_height()
    width = dpg.get_viewport_client_width()
    with dpg.window(label="Login to Chat Room", pos=(width//3, height//3), width=width//4):
        dpg.add_text('User Name: ')
        user_name = dpg.add_input_text()
        dpg.add_text('Password: ')
        password = dpg.add_input_text(password=True)
        error_reason = dpg.add_text(show=False, color=COLORS.RED)
        dpg.add_button(label="Login", user_data=(
            user_name, password, error_reason, client), callback=login)
        dpg.add_button(label="Create User", user_data=(
            user_name, password, error_reason, client), callback=create_user)
