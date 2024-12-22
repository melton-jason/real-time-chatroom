import dearpygui.dearpygui as dpg

from .colors import COLORS


def get_user_info(client):
    message_type, response = client.send_and_receive({
        "_message_type": "USERS",
    })
    if message_type == "OK":
        online, offline = response["online"], response["offline"]
        return {
            "online": filter(lambda name: name != client.username, online),
            "offline": offline
        }


def reset_list(sender, app_data, user_data):
    client = user_data
    parent = dpg.get_item_parent(sender)
    parent_pos = dpg.get_item_pos(parent)
    parent_width = dpg.get_item_width(parent)
    parent_height = dpg.get_item_height(parent)
    dpg.delete_item(parent)
    user_list(client, pos=parent_pos, width=parent_width, height=parent_height)


def user_list(client, pos=None, width=None, height=None):
    users = get_user_info(client)
    pos = (10, 20) if pos is None else pos
    width = 200 if width is None else width
    height = 120 if height is None else height
    with dpg.window(label="Users", pos=pos, width=width, height=height):
        dpg.add_button(label="Refresh", user_data=client, callback=reset_list)
        dpg.add_text("Other Online Users: ", color=COLORS.GREEN)
        for user in users["online"]:
            dpg.add_text(user)
        dpg.add_text("Offline Users: ", color=COLORS.GREY)
        dpg.add_combo(items=users["offline"])
