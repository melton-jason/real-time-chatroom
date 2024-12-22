import socket
import uuid
import threading

from settings import read_settings
from server.protocol import handle_message, send_ok
from server.database import setup_DB_connection

settings = read_settings()

HOST = settings['SERVER_HOST']
PORT = settings['SERVER_PORT']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server Listening on: {HOST}:{PORT}")
setup_DB_connection()


def handle(client: socket.socket):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '':
                continue
            client.send(handle_message(message))
        except Exception as e:
            client.close()


def receive():
    while True:
        client, address = server.accept()
        client.send(send_ok())
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
server.close()
