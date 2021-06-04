import requests
import json
import os
from requests.exceptions import HTTPError

class Config:

    def __init__(self, baseUri):
        self.baseUri = baseUri

    def GetConfig(self, route):
        try:
            response = requests.get(self.baseUri + route)
            if(response.status_code == 200):
                return json.loads(response.content.decode('utf-8'))
        except HTTPError as e:
            print("Failed to get probe configuration with message: " + e.message)
            quit()
    
    def __RegisterNewDevice(self, route):
        print(route)
