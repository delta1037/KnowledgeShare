# src from https://github.com/HugoLime/notion-backup/blob/master/notion_backup/configuration_service.py

import json
from json import JSONDecodeError

CONFIGURATION_FILE_NAME = "config.json"


class ConfigurationService:
    def __init__(self):
        self.conf_file = CONFIGURATION_FILE_NAME
        self._read_config()

    def get_key(self, key):
        return self.config.get(key)

    def write_key(self, key, value):
        self.config[key] = value
        self._save_config()

    def _read_config(self):
        try:
            with open(self.conf_file, "r", encoding="utf-8") as conf_file_handle:
                self.config = json.load(conf_file_handle)
        except FileNotFoundError:
            print("Configuration file does not exist")
        except JSONDecodeError:
            print("Configuration file is corrupted")

    def _save_config(self):
        with open(self.conf_file, "w+", encoding="utf-8") as conf_file_handle:
            json.dump(self.config, conf_file_handle, indent=4, sort_keys=False)


config = ConfigurationService()
