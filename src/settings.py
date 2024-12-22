import os
import json

from typing import TypedDict

SETTINGS_PATH = "settings.json"


class Settings(TypedDict):
    SERVER_HOST: str
    SERVER_PORT: int
    DB_PATH: str
    DB_SETUP: str


def read_settings() -> Settings:
    file = open(SETTINGS_PATH, 'r')
    settings = json.load(file)
    file.close()
    return settings
