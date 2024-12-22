import json
import socket

from typing import Tuple
from contextlib import contextmanager


def parse_message(message: str) -> Tuple[str, dict]:
    data: dict = json.loads(message)
    if not isinstance(data, dict):
        return ""
    message_type = data.get('_message_type', None)
    args = {k: v for k, v in data.items() if not k == '_message_type'}
    return message_type, args


def is_ok(response: bytes):
    try:
        message_type, args = parse_message(response.decode())
    except:
        return False
    return message_type == "OK"


class Client:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.client: socket.socket = None
        self.username = None
        self.id = None

    def connect(self):
        if self.client is not None:
            return self.client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.hostname, self.port))
            return is_ok(self.client.recv(1024))
        except:
            self.client.close()
        return False

    def send(self, data: dict):
        try:
            self.client.send(json.dumps({
                "USER": self.username,
                **data
            }).encode())
        except:
            self.client.close()

    def receive(self):
        try:
            message = self.client.recv(1024).decode()
            return parse_message(message)
        except:
            self.client.close()

    def send_and_receive(self, data: dict):
        try:
            self.send(data)
            return self.receive()
        except:
            self.client.close()
