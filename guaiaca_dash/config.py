import json
import os

class Config:
    def __init__(self) -> None:
        self.current_path= os.getcwd()

    def get_config(self, key):
        with open(self.current_path + '/guaiaca_dash/config.json', 'r') as file:
            config = json.load(file)
            return config[key]
        

