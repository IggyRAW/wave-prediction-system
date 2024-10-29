import json

CONFIG_FILE_PATH = "./config/config.json"


class ConfigManager:
    def __init__(self):
        self.config_path = CONFIG_FILE_PATH
        self.config = self._load()

    def _load(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_project(self, key):
        try:
            return self.config["project"][key]
        except KeyError:
            raise ValueError(f"key {key} not found in config")

    def get_path(self, key):
        try:
            return self.config["paths"][key]
        except KeyError:
            raise ValueError(f"key {key} not found in config")
