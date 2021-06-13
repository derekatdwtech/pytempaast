import json
import sys

class Config:

    def __init__(self):
        with open("config.json", 'r') as file:
            self.config = json.load(file)

    def GetApiUri(self):
        return self.config["ApiUri"]

    def GetApiHeaders(self):
        headers={'Api-Key': sys.argv[3], "Content-Type": "application/json"}
        return headers

    def GetTemperatureQueue(self):
        return self.config["TemperatureQueue"]

    def GetLogLevel(self):
        return self.config["logLevel"]