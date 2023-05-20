import json
from typing import Any

class Config(object):
    
    config_path = 'config.json'
    
    @classmethod
    def read_config(cls):
        with open(cls.config_path, 'r') as f:
            cls.config = json.load(f)
            return cls.config

    @classmethod
    def get(cls, key):
        if not hasattr(Config, 'config'):
            cls.read_config()
        return cls.config[key]
