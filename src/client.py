import dearpygui.dearpygui as dpg
import atexit

from client.connect import connection_window, handle_close

atexit.register(handle_close)

dpg.create_context()
dpg.create_viewport(title="ChatRoom")

connection_window()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
